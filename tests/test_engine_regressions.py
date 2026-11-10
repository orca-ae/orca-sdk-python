# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import asyncio
import threading
from typing import Any, AsyncIterator, cast
from concurrent.futures import ThreadPoolExecutor

import httpx2
import pytest
import pytest_asyncio
from respx import MockRouter

from orca import Orca, AsyncOrca, NotFoundError, APIConnectionError, InternalServerError, ExtensionNotAvailableError
from orca._base_client import BaseClient
from tests.api_resources.sessions.test_threads import THREAD
from tests.api_resources.test_engine_alignment import CATALOG

BASE_URL = "http://127.0.0.1:4010"
PRICING = "pricing.runorca.ai"


@pytest_asyncio.fixture(params=[False, True], ids=["sync", "async"])
async def review_client(request: pytest.FixtureRequest) -> AsyncIterator[Orca | AsyncOrca]:
    if request.param:
        async with AsyncOrca(api_key="k", base_url=BASE_URL, max_retries=0) as client:
            yield client
    else:
        with Orca(api_key="k", base_url=BASE_URL, max_retries=0) as sync_client:
            yield sync_client


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    now = [100.0]
    monkeypatch.setattr("orca._client.monotonic", lambda: now[0], raising=False)
    return now


def snapshot(version: str | None = "v1") -> dict[str, Any]:
    groups: list[dict[str, Any]] = [{"name": "cloud.sn.io"}]
    if version:
        groups.append({"name": PRICING, "versions": [{"version": version, "group_version": f"{PRICING}/{version}"}]})
    return {"groups": groups}


async def ensure(client: Orca | AsyncOrca, group: str = PRICING, version: str | None = "v2") -> None:
    if isinstance(client, AsyncOrca):
        await client._ensure_extension_available(group, version)
    else:
        client._ensure_extension_available(group, version)


def request(route: Any) -> httpx2.Request:
    return cast(httpx2.Request, route.calls[0].request)


def no_backoff(*_args: Any, **_kwargs: Any) -> float:
    return 0


@pytest.mark.respx(base_url=BASE_URL, assert_all_called=False)
@pytest.mark.parametrize("initial", ["v1", None], ids=["missing-version", "missing-group"])
async def test_discovery_missing_recovers_at_ttl(
    review_client: Orca | AsyncOrca, respx_mock: MockRouter, clock: list[float], initial: str | None
) -> None:
    root = respx_mock.get("/apis").mock(
        side_effect=[httpx2.Response(200, json=snapshot(initial)), httpx2.Response(200, json=snapshot("v2"))]
    )
    catalog = respx_mock.get("/apis/pricing.runorca.ai/v2/modelpricerules").respond(200, json=CATALOG)
    with pytest.raises(ExtensionNotAvailableError):
        await ensure(review_client)
    previous = review_client._extension_groups[str(review_client.base_url)]
    for age in [0.0, 14.999]:
        clock[0] = 100 + age
        with pytest.raises(ExtensionNotAvailableError):
            await ensure(review_client)
    assert root.call_count == 1
    clock[0] = 115
    if isinstance(review_client, AsyncOrca):
        page = await review_client.model_price_rules.list(extra_headers={"X-Test": "catalog"})
    else:
        page = review_client.model_price_rules.list(extra_headers={"X-Test": "catalog"})
    assert page.catalog_id == CATALOG["catalog_id"]
    assert root.call_count == 2
    assert f"{PRICING}/v2" not in previous
    assert request(catalog).headers["x-test"] == "catalog"
    clock[0] = 10000
    await ensure(review_client)
    assert root.call_count == 2


@pytest.mark.respx(base_url=BASE_URL)
@pytest.mark.parametrize("status", [503, 404])
async def test_discovery_refresh_failure_preserves_snapshot(
    review_client: Orca | AsyncOrca, respx_mock: MockRouter, clock: list[float], status: int
) -> None:
    root = respx_mock.get("/apis").mock(
        side_effect=[
            httpx2.Response(200, json=snapshot()),
            httpx2.Response(status, json={"error": "unavailable"}),
            httpx2.Response(200, json=snapshot("v2")),
        ]
    )
    await ensure(review_client, "cloud.sn.io", None)
    base = str(review_client.base_url)
    previous = review_client._extension_groups[base]
    clock[0] = 115
    with pytest.raises(NotFoundError if status == 404 else InternalServerError) as exc:
        await ensure(review_client)
    assert exc.value.status_code == status
    assert review_client._extension_groups[base] is previous
    assert review_client._extension_groups_fetched_at[base] == 100
    await ensure(review_client, "cloud.sn.io", None)
    await ensure(review_client, PRICING, "v1")
    assert root.call_count == 2
    await ensure(review_client)
    assert root.call_count == 3
    assert review_client._extension_groups_fetched_at[base] == 115


@pytest.mark.respx(base_url=BASE_URL, assert_all_called=False)
async def test_discovery_initial_404_is_warned_and_not_cached(
    review_client: Orca | AsyncOrca, respx_mock: MockRouter, clock: list[float], caplog: pytest.LogCaptureFixture
) -> None:
    root = respx_mock.get("/apis").mock(
        side_effect=[
            httpx2.Response(404, json={"error": "not found"}),
            httpx2.Response(404, json={"error": "not found"}),
            httpx2.Response(200, json=snapshot("v2")),
        ]
    )
    with caplog.at_level("WARNING", logger="orca._client"):
        for count in [1, 2]:
            with pytest.raises(ExtensionNotAvailableError):
                await ensure(review_client)
            assert root.call_count == count
            assert review_client._extension_groups == {}
            assert review_client._extension_groups_fetched_at == {}
    warnings = [record for record in caplog.records if "GET /apis is not served" in record.getMessage()]
    assert len(warnings) == 2
    await ensure(review_client)
    assert root.call_count == 3
    assert review_client._extension_groups_fetched_at[str(review_client.base_url)] == clock[0]


@pytest.mark.respx(base_url=BASE_URL)
async def test_discovery_refresh_still_missing_and_base_scoping(
    review_client: Orca | AsyncOrca, respx_mock: MockRouter, clock: list[float]
) -> None:
    root = respx_mock.get("/apis").respond(200, json=snapshot())
    for instant, count in [(100, 1), (115, 2), (129.999, 2), (130, 3)]:
        clock[0] = instant
        with pytest.raises(ExtensionNotAvailableError):
            await ensure(review_client)
        assert root.call_count == count
    other = respx_mock.get("http://other.example/apis").respond(200, json=snapshot("v2"))
    review_client.base_url = "http://other.example"
    await ensure(review_client)
    assert other.call_count == 1
    review_client.base_url = BASE_URL
    with pytest.raises(ExtensionNotAvailableError):
        await ensure(review_client)
    assert root.call_count == 3


@pytest.mark.respx(base_url=BASE_URL)
async def test_async_discovery_refresh_collapses(respx_mock: MockRouter, clock: list[float]) -> None:
    async with AsyncOrca(api_key="k", base_url=BASE_URL) as client:
        root = respx_mock.get("/apis").respond(200, json=snapshot())
        await client._ensure_extension_available(PRICING, "v1")
        clock[0] = 115
        entered, release = asyncio.Event(), asyncio.Event()

        async def refreshed(_request: httpx2.Request) -> httpx2.Response:
            entered.set()
            await release.wait()
            return httpx2.Response(200, json=snapshot("v2"))

        root.mock(side_effect=refreshed)
        calls = [asyncio.create_task(client._ensure_extension_available(PRICING, "v2")) for _ in range(4)]
        await asyncio.wait_for(entered.wait(), timeout=5)
        release.set()
        await asyncio.wait_for(asyncio.gather(*calls), timeout=5)
        assert root.call_count == 2


@pytest.mark.respx(base_url=BASE_URL)
def test_sync_discovery_refresh_collapses(respx_mock: MockRouter, clock: list[float]) -> None:
    with Orca(api_key="k", base_url=BASE_URL) as client:
        root = respx_mock.get("/apis").respond(200, json=snapshot())
        client._ensure_extension_available(PRICING, "v1")
        clock[0] = 115
        entered, release = threading.Event(), threading.Event()

        def refreshed(_request: httpx2.Request) -> httpx2.Response:
            entered.set()
            assert release.wait(timeout=5)
            return httpx2.Response(200, json=snapshot("v2"))

        root.mock(side_effect=refreshed)
        with ThreadPoolExecutor(max_workers=4) as pool:
            calls = [pool.submit(client._ensure_extension_available, PRICING, "v2") for _ in range(4)]
            assert entered.wait(timeout=5)
            release.set()
            for call in calls:
                call.result(timeout=5)
        assert root.call_count == 2


@pytest.mark.respx(base_url=BASE_URL)
@pytest.mark.parametrize("max_retries", [0, 2, 4])
@pytest.mark.parametrize("failure", ["502", "connection"])
async def test_interrupt_never_retries(
    review_client: Orca | AsyncOrca,
    respx_mock: MockRouter,
    monkeypatch: pytest.MonkeyPatch,
    max_retries: int,
    failure: str,
) -> None:
    monkeypatch.setattr(BaseClient, "_calculate_retry_timeout", no_backoff)
    review_client.max_retries = max_retries
    route = respx_mock.post("/v1/sessions/ses/threads/sth/interrupt")
    if failure == "502":
        route.respond(502, json={"error": "indexing failed"})
        error = InternalServerError
    else:
        route.mock(side_effect=httpx2.ConnectError("disconnected"))
        error = APIConnectionError
    with pytest.raises(error):
        if isinstance(review_client, AsyncOrca):
            await review_client.sessions.threads.interrupt("ses", "sth")
        else:
            review_client.sessions.threads.interrupt("ses", "sth")
    assert route.call_count == 1
    assert review_client.max_retries == max_retries
    read = respx_mock.get("/v1/sessions/ses/threads/sth").respond(502, json={"error": "unavailable"})
    with pytest.raises(InternalServerError):
        if isinstance(review_client, AsyncOrca):
            await review_client.sessions.threads.retrieve("ses", "sth")
        else:
            review_client.sessions.threads.retrieve("ses", "sth")
    assert read.call_count == max_retries + 1


@pytest.mark.respx(base_url=BASE_URL)
@pytest.mark.parametrize("extra_body", [None, {"extra": "value"}])
async def test_interrupt_preserves_options(
    review_client: Orca | AsyncOrca, respx_mock: MockRouter, extra_body: dict[str, str] | None
) -> None:
    route = respx_mock.post("/v1/sessions/ses%2Fone/threads/sth%2Fone/interrupt").respond(200, json=THREAD)
    options: dict[str, Any] = {
        "extra_headers": {"X-Test": "interrupt"},
        "extra_query": {"q": "1"},
        "extra_body": extra_body,
        "timeout": 3.0,
    }
    if isinstance(review_client, AsyncOrca):
        result = await review_client.sessions.threads.interrupt("ses/one", "sth/one", **options)
    else:
        result = review_client.sessions.threads.interrupt("ses/one", "sth/one", **options)
    assert result.id == THREAD["id"]
    sent = request(route)
    assert sent.url.raw_path == b"/v1/sessions/ses%2Fone/threads/sth%2Fone/interrupt?q=1"
    assert json.loads(sent.content) == (extra_body or {})
    assert sent.headers["content-type"] == "application/json"
    assert sent.headers["authorization"] == "Bearer k"
    assert sent.headers["x-test"] == "interrupt"
    assert sent.extensions["timeout"] == {"connect": 3.0, "read": 3.0, "write": 3.0, "pool": 3.0}
