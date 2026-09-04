from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.types.api_group import APIGroupList
from orca.types.api_resource import APIResourceList
from orca.resources.discovery import Discovery, AsyncDiscovery

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

GROUP_LIST: dict[str, Any] = {
    "kind": "APIGroupList",
    "groups": [
        {
            "name": "cloud.sn.io",
            "versions": [{"group_version": "cloud.sn.io/v1", "version": "v1"}],
            "preferred_version": {"group_version": "cloud.sn.io/v1", "version": "v1"},
        }
    ],
}

EMPTY_GROUP_LIST: dict[str, Any] = {"kind": "APIGroupList", "groups": []}

RESOURCE_LIST: dict[str, Any] = {
    "kind": "APIResourceList",
    "group_version": "policy.runorca.ai/v1",
    "resources": [{"name": "guardrails", "namespaced": True, "kind": "Guardrail"}],
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _sync(client: Orca) -> Discovery:
    """`Orca.discovery` is mounted in `_client.py`, which this change does not own;
    constructing the resource directly keeps these tests independent of that wiring
    while exercising exactly the same code path."""
    return Discovery(client)


def _async(client: AsyncOrca) -> AsyncDiscovery:
    return AsyncDiscovery(client)


class TestDiscovery:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_groups(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        groups = _sync(client).groups()
        assert_matches_type(APIGroupList, groups, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_groups_path_has_no_version_prefix(self, client: Orca, respx_mock: MockRouter) -> None:
        """`/apis` describes the deployment, not an API version, so it sits at the
        host root rather than under `/v1`."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        _sync(client).groups()
        assert _req(route).url.path == "/apis"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_groups_uses_wire_version_names(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        result = _sync(client).groups()
        assert result.kind == "APIGroupList"
        assert result.groups[0].name == "cloud.sn.io"
        assert result.groups[0].versions[0].group_version == "cloud.sn.io/v1"
        assert result.groups[0].versions[0].version == "v1"
        assert result.groups[0].preferred_version.group_version == "cloud.sn.io/v1"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_empty_groups_is_not_an_error(self, client: Orca, respx_mock: MockRouter) -> None:
        """No extensions installed is a normal deployment shape — it must parse, not
        raise. That is distinct from the 404 a pre-discovery deployment returns."""
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=EMPTY_GROUP_LIST))
        result = _sync(client).groups()
        assert_matches_type(APIGroupList, result, path=["response"])
        assert result.groups == []

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_groups(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        response = _sync(client).with_raw_response.groups()
        assert response.is_closed is True
        assert_matches_type(APIGroupList, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_groups(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        with _sync(client).with_streaming_response.groups() as response:
            assert not response.is_closed
            assert_matches_type(APIGroupList, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        _sync(client).groups(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"

    @parametrize
    @pytest.mark.parametrize(
        "group,path,method",
        [
            ("policy.runorca.ai", "/apis/policy.runorca.ai/v1", "policy_group_resources"),
            ("pricing.runorca.ai", "/apis/pricing.runorca.ai/v1", "pricing_group_resources"),
        ],
    )
    @pytest.mark.respx(base_url=base_url)
    def test_group_resource_discovery(
        self, client: Orca, respx_mock: MockRouter, group: str, path: str, method: str
    ) -> None:
        client._extension_groups.clear()
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json={"groups": [{"name": group}]}))
        route = respx_mock.get(path).mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        result = getattr(client.discovery, method)(extra_headers={"X-Test": "discovery"})
        assert_matches_type(APIResourceList, result, path=["response"])
        assert _req(route).headers["x-test"] == "discovery"

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_group_resource_discovery_is_gated(self, client: Orca, respx_mock: MockRouter) -> None:
        client._extension_groups.clear()
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=EMPTY_GROUP_LIST))
        route = respx_mock.get("/apis/policy.runorca.ai/v1").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        with pytest.raises(ExtensionNotAvailableError):
            client.discovery.policy_group_resources()
        assert route.called is False


class TestAsyncDiscovery:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_groups(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        groups = await _async(async_client).groups()
        assert_matches_type(APIGroupList, groups, path=["response"])
        assert _req(route).url.path == "/apis"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_empty_groups_is_not_an_error(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=EMPTY_GROUP_LIST))
        result = await _async(async_client).groups()
        assert result.groups == []

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_groups(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        response = await _async(async_client).with_raw_response.groups()
        assert response.is_closed is True
        assert_matches_type(APIGroupList, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_groups(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/apis").mock(return_value=httpx2.Response(200, json=GROUP_LIST))
        async with _async(async_client).with_streaming_response.groups() as response:
            assert not response.is_closed
            assert_matches_type(APIGroupList, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_policy_group_resource_discovery(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        async_client._extension_groups.clear()
        respx_mock.get("/apis").mock(
            return_value=httpx2.Response(200, json={"groups": [{"name": "policy.runorca.ai"}]})
        )
        respx_mock.get("/apis/policy.runorca.ai/v1").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        result = await async_client.discovery.policy_group_resources()
        assert_matches_type(APIResourceList, result, path=["response"])
