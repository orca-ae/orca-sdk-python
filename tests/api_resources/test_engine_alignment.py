# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import inspect
import warnings
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, APIStatusError, APIResponseValidationError, ExtensionNotAvailableError
from orca.types import GuardrailDogwoodRule, GuardrailUnknownRule
from orca.resources.discovery import Discovery, AsyncDiscovery
from orca.resources.guardrails import Guardrails, AsyncGuardrails
from orca.resources.environments import Environments, AsyncEnvironments
from orca.resources.sessions.threads import Threads, AsyncThreads
from orca.resources.model_price_rules import ModelPriceRules, AsyncModelPriceRules
from tests.api_resources.test_guardrails import GUARDRAIL
from tests.api_resources.test_environments import ENVIRONMENT
from tests.api_resources.sessions.test_threads import THREAD

BASE_URL = "http://127.0.0.1:4010"
POLICY = "/apis/policy.runorca.ai/v1"
PRICING = "/apis/pricing.runorca.ai/v2"

DOGWOOD: dict[str, Any] = {
    "kind": "dogwood",
    "policy": "permit(principal, action, resource);",
    "applies_to": "mcp_tools",
    "history": "principal",
    "mcp_manifests": [{"server": "tools", "url": "https://tools.example/mcp", "tools": [{"name": "read"}]}],
}
BUNDLE: dict[str, Any] = {
    "schema": "1",
    "bundle_id": "registry-one",
    "generation": 1,
    "scope": {"org_id": "org_one", "workspace_id": "ws_one"},
    "runtime_config_revision": "r1",
    "issued_at": "2026-11-09T00:00:00Z",
    "expires_at": "2026-11-09T01:00:00Z",
    "seed_verdict": "allow",
    "guardrails": [
        {
            "id": "grd_one",
            "name": "budget",
            "tier": "workspace",
            "phases": ["request"],
            "rule": {"kind": "future", "payload": 1},
            "stateful": True,
            "mode": "observe",
            "state_scope": "workspace_window",
        }
    ],
    "omitted_rules": 0,
}
LEASE_HEADERS = {
    "ETag": '"registry-' + "a" * 64 + '"',
    "Cache-Control": "no-store",
    "Orca-Guardrail-Issued-At": BUNDLE["issued_at"],
    "Orca-Guardrail-Expires-At": BUNDLE["expires_at"],
    "Orca-Guardrail-Generation": "1",
}
RULE: dict[str, Any] = {
    "conditions": {"service_tier": "standard", "request_input_tokens": {"min": 0, "max": None}},
    "rates": {
        "input_per_million_tokens": 3,
        "output_per_million_tokens": 15,
        "cache_read_per_million_tokens": None,
        "cache_write_per_million_tokens": None,
        "cache_write_1h_per_million_tokens": None,
    },
    "rule_set_id": "set_one",
    "rule_id": "rule_one",
    "revision": 1,
    "provider": "provider",
    "model_id": "model",
    "source": "operator",
    "usage_profile": "exclusive-v1",
    "profile_version": "1",
    "provenance": {
        "source_id": "source",
        "document_sha256": "digest",
        "adapter_version": "1",
        "observed_at": BUNDLE["issued_at"],
    },
    "provider_effective_at": None,
    "active_from": BUNDLE["issued_at"],
    "retired_at": None,
    "valid_until": None,
}
CATALOG: dict[str, Any] = {
    "catalog_id": "cat_one",
    "generation": 7,
    "digest": "sha256-one",
    "published_at": BUNDLE["issued_at"],
    "expires_at": BUNDLE["expires_at"],
    "required_features": ["future.feature.v9"],
    "conditional_models": [{"provider": "provider", "model_id": "model"}],
    "data": [RULE],
    "next_page": "cursor-one",
}
SCHEMA = {
    "base_schema": "base",
    "event_schemas": {"session": "session", "principal": "principal"},
    "language_version": "1",
    "core_version": "1",
    "limits": {"future_limit": 42},
}


def gate(router: MockRouter, client: Orca | AsyncOrca, *, version: str = "v2") -> None:
    client._extension_groups.clear()
    groups: list[dict[str, Any]] = []
    for name, v in [("policy.runorca.ai", "v1"), ("pricing.runorca.ai", version), ("runtime.runorca.ai", "v1")]:
        groups.append({"name": name, "versions": [{"version": v, "group_version": f"{name}/{v}"}]})
    router.get("/apis").respond(200, json={"kind": "APIGroupList", "groups": groups})


def request(route: Any, index: int = 0) -> httpx2.Request:
    return cast("httpx2.Request", route.calls[index].request)


def assert_catalog(page: Any) -> None:
    for key in ["catalog_id", "generation", "digest", "published_at", "expires_at", "required_features"]:
        assert getattr(page, key) == CATALOG[key]
    assert page.conditional_models[0].model_id == "model"
    assert page.data[0].conditions.request_input_tokens.max is None


@pytest.mark.parametrize("client", [False, True], indirect=True)
@pytest.mark.respx(base_url=BASE_URL)
def test_dogwood_and_future_roundtrip(client: Orca, respx_mock: MockRouter) -> None:
    gate(respx_mock, client)
    route = respx_mock.post(POLICY + "/guardrails").respond(
        201, json={**GUARDRAIL, "rule": DOGWOOD, "mode": "observe", "warnings": ["review"]}
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = client.guardrails.create(name="policy", rule=cast(Any, DOGWOOD), mode="observe")
        assert isinstance(result.rule, GuardrailDogwoodRule)
        assert result.model_dump(exclude_unset=True)["rule"] == DOGWOOD
        assert result.rule.model_dump_json(exclude_unset=True)
    assert result.mode == "observe" and result.warnings == ["review"]
    assert json.loads(request(route).content)["mode"] == "observe"
    future = {"kind": "future", "nested": {"values": [1, 2]}}
    update = respx_mock.post(POLICY + "/guardrails/grd_one").respond(200, json={**GUARDRAIL, "rule": future})
    result = client.guardrails.update("grd_one", mode="enforce")
    assert isinstance(result.rule, GuardrailUnknownRule)
    assert result.model_dump(exclude_unset=True)["rule"] == future
    assert json.loads(request(update).content) == {"mode": "enforce"}


@pytest.mark.parametrize("client", [False, True], indirect=True)
@pytest.mark.parametrize(
    "rule", [{"kind": "dogwood"}, {"kind": "builtin"}, {"kind": "expression", "expression": "true"}]
)
@pytest.mark.respx(base_url=BASE_URL)
def test_malformed_known_rules_cannot_use_unknown_fallback(
    client: Orca, respx_mock: MockRouter, rule: dict[str, Any]
) -> None:
    gate(respx_mock, client)
    respx_mock.get(POLICY + "/guardrails/grd_one").respond(200, json={**GUARDRAIL, "rule": rule})
    if client._strict_response_validation:
        with pytest.raises(APIResponseValidationError):
            client.guardrails.retrieve("grd_one")
    else:
        # Loose parsing keeps its normal tolerance, but still selects the known variant.
        result = client.guardrails.retrieve("grd_one")
        assert not isinstance(result.rule, GuardrailUnknownRule)
        assert result.rule.kind == rule["kind"]


@pytest.mark.parametrize("client", [False, True], indirect=True)
@pytest.mark.respx(base_url=BASE_URL)
def test_legacy_guardrail_without_mode(client: Orca, respx_mock: MockRouter) -> None:
    gate(respx_mock, client)
    legacy = {key: value for key, value in GUARDRAIL.items() if key != "mode"}
    respx_mock.get(POLICY + "/guardrails/grd_one").respond(200, json=legacy)
    result = client.guardrails.retrieve("grd_one")
    assert result.mode is None
    assert "mode" not in result.model_dump(exclude_unset=True)


@pytest.mark.parametrize("client", [False, True], indirect=True)
@pytest.mark.respx(base_url=BASE_URL)
def test_effective_raw_stream_and_scoped_304(client: Orca, respx_mock: MockRouter) -> None:
    gate(respx_mock, client)
    route = respx_mock.get(POLICY + "/effectiveguardrails").respond(200, json=BUNDLE, headers=LEASE_HEADERS)
    raw = client.with_raw_response.guardrails.effective(
        rule_kinds="builtin,dogwood",
        guardrail_capabilities="guardrails.observe.v1",
        if_none_match="old",
        extra_headers={"X-Test": "yes"},
        extra_query={"rule_kinds": "dogwood"},
        timeout=4,
    )
    bundle = raw.parse()
    assert bundle is not None and bundle.guardrails[0].state_scope == "workspace_window"
    assert bundle.to_dict()["schema"] == "1"
    assert raw.headers["etag"] == LEASE_HEADERS["ETag"]
    assert dict(request(route).url.params) == {
        "rule_kinds": "dogwood",
        "guardrail_capabilities": "guardrails.observe.v1",
    }
    assert request(route).headers["if-none-match"] == "old"
    assert request(route).extensions["timeout"]["read"] == 4
    route.respond(304, content=b"not-json", headers={**LEASE_HEADERS, "content-type": "application/json"})
    raw = client.guardrails.with_raw_response.effective(if_none_match=LEASE_HEADERS["ETag"])
    assert raw.status_code == 304 and raw.parse() is None
    assert raw.headers["orca-guardrail-expires-at"] == BUNDLE["expires_at"]
    assert client.guardrails.effective() is None
    assert not request(route, 2).url.params
    with client.with_streaming_response.guardrails.effective() as stream:
        assert stream.parse() is None
        assert stream.headers["orca-guardrail-generation"] == "1"
    assert route.call_count == 4
    other = respx_mock.get(POLICY + "/policyschemas/dogwood").respond(304)
    with pytest.raises(APIStatusError) as exc:
        client.guardrails.dogwood_schema()
    assert exc.value.status_code == 304 and other.call_count == 1


@pytest.mark.parametrize("client", [False, True], indirect=True)
@pytest.mark.respx(base_url=BASE_URL)
def test_pricing_pages_keep_metadata_options_and_stop_on_410(client: Orca, respx_mock: MockRouter) -> None:
    gate(respx_mock, client)
    route = respx_mock.get(PRICING + "/modelpricerules").mock(
        side_effect=[
            httpx2.Response(200, json=CATALOG),
            httpx2.Response(200, json={**CATALOG, "next_page": "cursor-two"}),
            httpx2.Response(410, json={"error": {"message": "catalog expired"}}),
        ]
    )
    first = client.model_price_rules.list(
        limit=1, extra_headers={"X-Test": "pages"}, extra_query={"custom": "x"}, timeout=3
    )
    assert_catalog(first)
    second = first.get_next_page()
    assert_catalog(second)
    assert dict(request(route, 1).url.params) == {"limit": "1", "page": "cursor-one", "custom": "x"}
    assert request(route, 1).headers["x-test"] == "pages"
    assert request(route, 1).extensions["timeout"]["read"] == 3
    with pytest.raises(APIStatusError) as exc:
        second.get_next_page()
    assert exc.value.status_code == 410 and route.call_count == 3


@pytest.mark.respx(base_url=BASE_URL)
def test_pricing_v1_only_gate(client: Orca, respx_mock: MockRouter) -> None:
    gate(respx_mock, client, version="v1")
    for call in [client.model_price_rules.list, client.discovery.pricing_v2_group_resources]:
        with pytest.raises(ExtensionNotAvailableError):
            call()
    assert len(respx_mock.calls) == 1


@pytest.mark.parametrize("async_client", [False, True], indirect=True)
@pytest.mark.respx(base_url=BASE_URL)
async def test_async_dogwood_modes_and_unknown(async_client: AsyncOrca, respx_mock: MockRouter) -> None:
    gate(respx_mock, async_client)
    route = respx_mock.post(POLICY + "/guardrails").respond(
        201, json={**GUARDRAIL, "rule": DOGWOOD, "warnings": ["review"]}
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = await async_client.guardrails.create(name="policy", rule=cast(Any, DOGWOOD), mode="observe")
        assert isinstance(result.rule, GuardrailDogwoodRule)
        assert result.model_dump(exclude_unset=True)["rule"] == DOGWOOD
    assert json.loads(request(route).content)["mode"] == "observe"
    future = {"kind": "future", "policy_v2": {"key": "value"}}
    route = respx_mock.post(POLICY + "/guardrails/grd_one").respond(200, json={**GUARDRAIL, "rule": future})
    result = await async_client.guardrails.update("grd_one", mode="enforce")
    assert isinstance(result.rule, GuardrailUnknownRule)
    assert result.model_dump(exclude_unset=True)["rule"] == future
    assert json.loads(request(route).content) == {"mode": "enforce"}


@pytest.mark.parametrize("async_client", [False, True], indirect=True)
@pytest.mark.respx(base_url=BASE_URL)
async def test_async_effective_and_catalog(async_client: AsyncOrca, respx_mock: MockRouter) -> None:
    gate(respx_mock, async_client)
    route = respx_mock.get(POLICY + "/effectiveguardrails").respond(200, json=BUNDLE, headers=LEASE_HEADERS)
    raw = await async_client.with_raw_response.guardrails.effective(
        rule_kinds="dogwood", guardrail_capabilities="future", if_none_match="old"
    )
    bundle = await raw.parse()
    assert bundle is not None and bundle.guardrails[0].mode == "observe"
    assert request(route).headers["if-none-match"] == "old"
    assert request(route).url.params["guardrail_capabilities"] == "future"
    route.respond(304, content=b"not-json", headers=LEASE_HEADERS)
    raw = await async_client.guardrails.with_raw_response.effective()
    assert raw.status_code == 304 and await raw.parse() is None
    assert raw.headers["etag"] == LEASE_HEADERS["ETag"]
    assert await async_client.guardrails.effective() is None
    async with async_client.with_streaming_response.guardrails.effective() as stream:
        assert await stream.parse() is None
    assert route.call_count == 4
    prices = respx_mock.get(PRICING + "/modelpricerules").mock(
        side_effect=[
            httpx2.Response(200, json=CATALOG),
            httpx2.Response(200, json=CATALOG),
            httpx2.Response(410, json={"error": {"message": "expired"}}),
        ]
    )
    first = await async_client.model_price_rules.list(limit=1, extra_headers={"X-Test": "async"})
    assert_catalog(first)
    second = await first.get_next_page()
    assert_catalog(second)
    assert request(prices, 1).url.params["page"] == "cursor-one"
    assert request(prices, 1).headers["x-test"] == "async"
    with pytest.raises(APIStatusError) as exc:
        await second.get_next_page()
    assert exc.value.status_code == 410 and prices.call_count == 3


@pytest.mark.respx(base_url=BASE_URL)
async def test_async_v1_gate_and_malformed_known(async_client: AsyncOrca, respx_mock: MockRouter) -> None:
    gate(respx_mock, async_client, version="v1")
    with pytest.raises(ExtensionNotAvailableError):
        await async_client.model_price_rules.list()
    with pytest.raises(ExtensionNotAvailableError):
        await async_client.discovery.pricing_v2_group_resources()
    respx_mock.get(POLICY + "/guardrails/grd_one").respond(200, json={**GUARDRAIL, "rule": {"kind": "dogwood"}})
    with pytest.raises(APIResponseValidationError):
        await async_client.guardrails.retrieve("grd_one")


@pytest.mark.parametrize("client", [False, True], indirect=True)
@pytest.mark.respx(base_url=BASE_URL)
def test_historical_paths_and_discovery(client: Orca, respx_mock: MockRouter) -> None:
    gate(respx_mock, client)
    rotate = respx_mock.post("/v1/environments/env%2Fone/rotate-key").respond(
        200, json={"env_key": "secret", "env_key_expires_at": BUNDLE["expires_at"]}
    )
    assert (
        client.environments.rotate_key("env/one", extra_headers={"idempotency-key": "key"}, timeout=2).env_key
        == "secret"
    )
    assert request(rotate).url.raw_path == b"/v1/environments/env%2Fone/rotate-key"
    assert json.loads(request(rotate).content) == {}
    assert request(rotate).headers["content-type"] == "application/json"
    assert request(rotate).headers["idempotency-key"] == "key"
    revoke = respx_mock.post("/v1/environments/env%2Fone/revoke-key").respond(200, json=ENVIRONMENT)
    assert client.environments.revoke_key("env/one").id == ENVIRONMENT["id"]
    assert json.loads(request(revoke).content) == {}
    assert request(revoke).headers["content-type"] == "application/json"
    stats = respx_mock.get("/v1/environments/env%2Fone/work_stats").respond(
        200, json={"depth": 1, "in_flight": 2, "worker_connected": True}
    )
    assert client.environments.work_stats("env/one").in_flight == 2
    assert not request(stats).content
    interrupt = respx_mock.post("/v1/sessions/ses%2Fone/threads/sth%2Fone/interrupt").respond(200, json=THREAD)
    assert (
        client.sessions.threads.interrupt("ses/one", "sth/one", extra_headers={"orca-beta": "test"}).id == THREAD["id"]
    )
    assert json.loads(request(interrupt).content) == {}
    assert request(interrupt).headers["content-type"] == "application/json"
    assert request(interrupt).headers["orca-beta"] == "test"
    for path, method in [
        ("/apis/runtime.runorca.ai/v1", client.discovery.runtime_group_resources),
        ("/apis/pricing.runorca.ai/v2", client.discovery.pricing_v2_group_resources),
    ]:
        respx_mock.get(path).respond(
            200,
            json={
                "kind": "APIResourceList",
                "group_version": path.removeprefix("/apis/"),
                "resources": [],
                "required_features": ["future.feature"],
            },
        )
        assert method().required_features == ["future.feature"]
    respx_mock.get("/apis/runtime.runorca.ai/v1/harnesses").respond(
        200,
        json={
            "data": [
                {
                    "id": "test",
                    "provider": "provider",
                    "modes": ["future"],
                    "capabilities": {"managed_skills": True, "multiagent": False, "native_resume": True},
                    "models": [{"provider": "provider", "id": "model", "efforts": ["future"]}],
                }
            ]
        },
    )
    assert client.discovery.harnesses().data[0].models[0].efforts == ["future"]
    respx_mock.get(POLICY + "/policyschemas/dogwood").respond(200, json=SCHEMA)
    assert client.guardrails.dogwood_schema().event_schemas.principal == "principal"


def test_sync_async_signatures_match() -> None:
    for sync, async_, names in [
        (Guardrails, AsyncGuardrails, ["create", "update", "effective", "dogwood_schema"]),
        (Environments, AsyncEnvironments, ["rotate_key", "revoke_key", "work_stats"]),
        (Discovery, AsyncDiscovery, ["runtime_group_resources", "harnesses", "pricing_v2_group_resources"]),
        (Threads, AsyncThreads, ["interrupt"]),
        (ModelPriceRules, AsyncModelPriceRules, ["list"]),
    ]:
        for name in names:
            assert (
                inspect.signature(getattr(sync, name)).parameters == inspect.signature(getattr(async_, name)).parameters
            )


@pytest.mark.parametrize("async_client", [False, True], indirect=True)
@pytest.mark.parametrize("wrapper", ["direct", "with_raw_response", "with_streaming_response"])
@pytest.mark.respx(base_url=BASE_URL)
async def test_async_historical_methods_and_wrappers(
    async_client: AsyncOrca, respx_mock: MockRouter, wrapper: str
) -> None:
    gate(respx_mock, async_client)
    target = cast(Any, async_client if wrapper == "direct" else getattr(async_client, wrapper))
    calls: list[tuple[str, str, Any, list[str], dict[str, Any], str, Any]] = [
        (
            "POST",
            "/v1/environments/env%2Fone/rotate-key",
            target.environments.rotate_key,
            ["env/one"],
            {"env_key": "secret", "env_key_expires_at": BUNDLE["expires_at"]},
            "env_key",
            "secret",
        ),
        (
            "POST",
            "/v1/environments/env%2Fone/revoke-key",
            target.environments.revoke_key,
            ["env/one"],
            ENVIRONMENT,
            "id",
            ENVIRONMENT["id"],
        ),
        (
            "GET",
            "/v1/environments/env%2Fone/work_stats",
            target.environments.work_stats,
            ["env/one"],
            {"depth": 3, "in_flight": 1, "worker_connected": False},
            "depth",
            3,
        ),
        (
            "POST",
            "/v1/sessions/ses%2Fone/threads/sth%2Fone/interrupt",
            target.sessions.threads.interrupt,
            ["ses/one", "sth/one"],
            THREAD,
            "id",
            THREAD["id"],
        ),
        (
            "GET",
            "/apis/runtime.runorca.ai/v1",
            target.discovery.runtime_group_resources,
            [],
            {"kind": "APIResourceList", "group_version": "runtime.runorca.ai/v1", "resources": []},
            "group_version",
            "runtime.runorca.ai/v1",
        ),
        ("GET", "/apis/runtime.runorca.ai/v1/harnesses", target.discovery.harnesses, [], {"data": []}, "data", []),
        (
            "GET",
            "/apis/pricing.runorca.ai/v2",
            target.discovery.pricing_v2_group_resources,
            [],
            {
                "kind": "APIResourceList",
                "group_version": "pricing.runorca.ai/v2",
                "resources": [],
                "required_features": ["future"],
            },
            "required_features",
            ["future"],
        ),
        (
            "GET",
            "/apis/policy.runorca.ai/v1/policyschemas/dogwood",
            target.guardrails.dogwood_schema,
            [],
            SCHEMA,
            "base_schema",
            "base",
        ),
        (
            "GET",
            "/apis/pricing.runorca.ai/v2/modelpricerules",
            target.model_price_rules.list,
            [],
            {**CATALOG, "next_page": None},
            "catalog_id",
            CATALOG["catalog_id"],
        ),
    ]
    for method, path, call, args, payload, field, expected in calls:
        route = respx_mock.route(method=method, url=BASE_URL + path).respond(200, json=payload)
        options = {"extra_headers": {"idempotency-key": "one", "orca-beta": "test"}, "timeout": 2}
        if wrapper == "with_streaming_response":
            async with call(*args, **options) as raw:
                result = await raw.parse()
        else:
            result = await call(*args, **options)
            if wrapper == "with_raw_response":
                result = await result.parse()
        assert getattr(result, field) == expected
        assert request(route).url.raw_path == path.encode()
        assert request(route).headers["idempotency-key"] == "one"
        assert request(route).headers["orca-beta"] == "test"
        assert request(route).extensions["timeout"]["read"] == 2
        assert request(route).content == (b"{}" if method == "POST" else b"")
        if method == "POST":
            assert request(route).headers["content-type"] == "application/json"
