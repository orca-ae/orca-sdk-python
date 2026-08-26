"""Behaviours specific to this SDK, ported from the TypeScript client's test suite.

The inherited `test_client.py` covers the shared transport (retries, headers, query
merging, response parsing). This file covers what is particular to this API: the
legacy base-URL shim, callable credentials, and extension gating.
"""

from __future__ import annotations

import asyncio
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, OrcaError, ExtensionNotAvailableError
from orca._models import FinalRequestOptions

base_url = "http://127.0.0.1:4010"


def _auth(client: Orca | AsyncOrca) -> str | None:
    request = client._build_request(FinalRequestOptions(method="get", url="/v1/agents"))
    return request.headers.get("authorization")


class TestBaseURL:
    def test_required_when_absent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ORCA_BASE_URL", raising=False)
        with pytest.raises(OrcaError, match="base_url is required"):
            Orca(api_key="k")

    def test_read_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ORCA_BASE_URL", "https://env.example")
        assert str(Orca(api_key="k").base_url).rstrip("/") == "https://env.example"

    @pytest.mark.parametrize(
        "given,expected",
        [
            ("https://h.example/v1", "https://h.example"),
            ("https://h.example/v1/registry", "https://h.example"),
            ("https://h.example/api/v1", "https://h.example"),
            ("https://h.example/v1/", "https://h.example"),
            ("https://h.example/base/v1", "https://h.example/base"),
        ],
    )
    def test_strips_legacy_suffixes(self, given: str, expected: str) -> None:
        client = Orca(api_key="k", base_url=given)
        assert str(client.base_url).rstrip("/") == expected

    @pytest.mark.parametrize(
        "given",
        [
            "https://h.example",
            "https://h.example/v1/extra",
            "http://v1",
            "https://h.example/v2",
        ],
    )
    def test_leaves_other_urls_alone(self, given: str) -> None:
        client = Orca(api_key="k", base_url=given)
        assert str(client.base_url).rstrip("/") == given.rstrip("/")

    def test_api_v1_strips_whole_suffix(self) -> None:
        """`/api/v1` must not degrade to `/api`.

        Core paths would still resolve there through the `/api/v1/*` alias while every
        `/apis/...` extension call silently 404s -- half the surface broken with nothing
        to notice. Stripping the whole suffix leaves the real host root.
        """
        client = Orca(api_key="k", base_url="https://h.example/api/v1")
        core = client._build_request(FinalRequestOptions(method="get", url="/v1/agents"))
        ext = client._build_request(FinalRequestOptions(method="get", url="/apis/cloud.sn.io/v1/connections"))
        assert str(core.url) == "https://h.example/v1/agents"
        assert str(ext.url) == "https://h.example/apis/cloud.sn.io/v1/connections"

    def test_warns_once_on_legacy_suffix(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level("WARNING", logger="orca._client"):
            Orca(api_key="k", base_url="https://h.example/v1")
        warnings = [r for r in caplog.records if "no longer part of the base URL" in r.getMessage()]
        assert len(warnings) == 1


class TestApiKey:
    def test_literal(self) -> None:
        assert _auth(Orca(api_key="secret", base_url=base_url)) == "Bearer secret"

    def test_env_fallback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ORCA_API_KEY", "from-env")
        assert _auth(Orca(base_url=base_url)) == "Bearer from-env"

    def test_explicit_none_disables_auth(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ORCA_API_KEY", "from-env")
        assert _auth(Orca(api_key=None, base_url=base_url)) is None

    def test_callable_is_invoked_per_request(self) -> None:
        calls: list[int] = []

        def rotating() -> str:
            calls.append(1)
            return f"token-{len(calls)}"

        client = Orca(api_key=rotating, base_url=base_url)
        assert _auth(client) == "Bearer token-1"
        assert _auth(client) == "Bearer token-2"
        assert len(calls) == 2

    def test_callable_returning_empty_raises(self) -> None:
        client = Orca(api_key=lambda: "", base_url=base_url)
        with pytest.raises(OrcaError, match="non-empty string"):
            _auth(client)

    async def test_async_callable(self) -> None:
        async def fetch() -> str:
            await asyncio.sleep(0)
            return "async-token"

        client = AsyncOrca(api_key=fetch, base_url=base_url)
        options = await client._prepare_options(FinalRequestOptions(method="get", url="/v1/agents"))
        assert cast(Any, options.headers)["Authorization"] == "Bearer async-token"

    async def test_async_sync_callable(self) -> None:
        client = AsyncOrca(api_key=lambda: "sync-token", base_url=base_url)
        options = await client._prepare_options(FinalRequestOptions(method="get", url="/v1/agents"))
        assert cast(Any, options.headers)["Authorization"] == "Bearer sync-token"


def _groups(*names: str) -> dict[str, Any]:
    return {"kind": "APIGroupList", "groups": [{"name": n} for n in names]}


class TestExtensionGating:
    @pytest.mark.respx(base_url=base_url)
    def test_resolves_when_group_is_served(self, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=_groups("cloud.sn.io")))
        client = Orca(api_key="k", base_url=base_url)
        client._ensure_extension_available("cloud.sn.io")

    @pytest.mark.respx(base_url=base_url)
    def test_raises_when_group_absent(self, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=_groups("other.group")))
        client = Orca(api_key="k", base_url=base_url)
        with pytest.raises(ExtensionNotAvailableError) as excinfo:
            client._ensure_extension_available("cloud.sn.io")
        assert excinfo.value.group == "cloud.sn.io"

    @pytest.mark.respx(base_url=base_url)
    def test_empty_groups_is_not_an_error_condition(self, respx_mock: MockRouter) -> None:
        """An empty `groups` array means "no extensions installed", not a failure."""
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=_groups()))
        client = Orca(api_key="k", base_url=base_url)
        with pytest.raises(ExtensionNotAvailableError):
            client._ensure_extension_available("cloud.sn.io")

    @pytest.mark.respx(base_url=base_url)
    def test_missing_discovery_route_is_treated_as_no_extensions(self, respx_mock: MockRouter) -> None:
        """A deployment predating `GET /apis` serves no extensions.

        It must surface as ExtensionNotAvailableError, never as a raw NotFoundError --
        the caller asked about a namespace, not about `/apis`.
        """
        respx_mock.get("/apis").mock(return_value=httpx2.Response(404, json={"error": {"type": "not_found"}}))
        client = Orca(api_key="k", base_url=base_url, max_retries=0)
        with pytest.raises(ExtensionNotAvailableError):
            client._ensure_extension_available("cloud.sn.io")

    @pytest.mark.respx(base_url=base_url)
    def test_result_is_cached_across_calls(self, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=_groups("cloud.sn.io")))
        client = Orca(api_key="k", base_url=base_url)
        for _ in range(3):
            client._ensure_extension_available("cloud.sn.io")
        assert route.call_count == 1

    @pytest.mark.respx(base_url=base_url)
    async def test_async_gate(self, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=_groups("cloud.sn.io")))
        client = AsyncOrca(api_key="k", base_url=base_url)
        await asyncio.gather(*(client._ensure_extension_available("cloud.sn.io") for _ in range(3)))
        # concurrent first-callers share a single probe rather than stampeding
        assert route.call_count == 1

    @pytest.mark.respx(base_url=base_url)
    async def test_async_raises_when_absent(self, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=_groups()))
        client = AsyncOrca(api_key="k", base_url=base_url)
        with pytest.raises(ExtensionNotAvailableError):
            await client._ensure_extension_available("cloud.sn.io")


def test_extension_error_is_not_an_api_error() -> None:
    """Gating happens before any HTTP request, so there is no response to attach."""
    from orca import APIError

    assert issubclass(ExtensionNotAvailableError, OrcaError)
    assert not issubclass(ExtensionNotAvailableError, APIError)
