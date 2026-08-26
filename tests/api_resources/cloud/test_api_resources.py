from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.resources.cloud import Cloud, AsyncCloud
from orca.types.cloud_api_resource import CloudAPIResourceList

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

RESOURCE_LIST: dict[str, Any] = {
    "kind": "APIResourceList",
    "group_version": "cloud.sn.io/v1",
    "resources": [
        {"name": "connections", "namespaced": False, "kind": "Connection"},
        {"name": "functions", "namespaced": True, "kind": "Function"},
    ],
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _gate(respx_mock: MockRouter, client: Orca | AsyncOrca, *, available: bool = True) -> Any:
    """Stub `GET /apis` and drop any discovery result the client already cached.

    Discovery is cached per base URL and the client fixture is session-scoped, so
    without the reset whichever cloud test ran first would decide the answer for
    every test after it.
    """
    client._extension_groups.clear()
    groups = [{"name": "cloud.sn.io"}] if available else []
    return respx_mock.get("/apis").mock(
        return_value=httpx2.Response(200, json={"kind": "APIGroupList", "groups": groups})
    )


class TestAPIResources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        resources = Cloud(client).api_resources.list()
        assert_matches_type(CloudAPIResourceList, resources, path=["response"])
        assert _req(route).method == "GET"
        assert resources.group_version == "cloud.sn.io/v1"
        assert resources.resources[0].name == "connections"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_group_root_keeps_its_trailing_slash(self, client: Orca, respx_mock: MockRouter) -> None:
        """The group root is `.../v1/`; dropping the slash is a different route."""
        _gate(respx_mock, client)
        route = respx_mock.get(url__regex=r".*cloud\.sn\.io.*").mock(
            return_value=httpx2.Response(200, json=RESOURCE_LIST)
        )
        Cloud(client).api_resources.list()
        assert str(_req(route).url).endswith("/apis/cloud.sn.io/v1/")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        response = Cloud(client).api_resources.with_raw_response.list()
        assert response.is_closed is True
        assert_matches_type(CloudAPIResourceList, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        with Cloud(client).api_resources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert_matches_type(CloudAPIResourceList, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.get(url__regex=r".*cloud\.sn\.io.*").mock(
            return_value=httpx2.Response(200, json=RESOURCE_LIST)
        )
        with pytest.raises(ExtensionNotAvailableError):
            Cloud(client).api_resources.list()
        assert route.called is False


class TestAsyncAPIResources:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        resources = await AsyncCloud(async_client).api_resources.list()
        assert_matches_type(CloudAPIResourceList, resources, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        response = await AsyncCloud(async_client).api_resources.with_raw_response.list()
        assert response.is_closed is True
        assert_matches_type(CloudAPIResourceList, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/").mock(return_value=httpx2.Response(200, json=RESOURCE_LIST))
        async with AsyncCloud(async_client).api_resources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert_matches_type(CloudAPIResourceList, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get(url__regex=r".*cloud\.sn\.io.*").mock(
            return_value=httpx2.Response(200, json=RESOURCE_LIST)
        )
        with pytest.raises(ExtensionNotAvailableError):
            await AsyncCloud(async_client).api_resources.list()
        assert route.called is False
