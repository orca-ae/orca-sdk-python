from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.resources.cloud import Cloud, AsyncCloud
from orca.types.cloud_agent_provider import CloudAgentProvider, CloudAgentProviderList

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

PROVIDER: dict[str, Any] = {
    "name": "primary",
    "type": "chat",
    "api_url": "https://models.test/v1",
    "api_version": "2026-01-01",
    "beta_version": None,
    "api_key_env": "PRIMARY_API_KEY",
    "api_key_configured": True,
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


class TestProviders:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/agents/providers").mock(
            return_value=httpx2.Response(200, json=[PROVIDER])
        )
        providers = Cloud(client).agents.providers.list()
        assert_matches_type(CloudAgentProviderList, providers, path=["response"])
        assert _req(route).method == "GET"
        assert providers[0].api_key_configured is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_tolerates_sparse_entries(self, client: Orca, respx_mock: MockRouter) -> None:
        """Every provider field is optional in the contract, including `name`."""
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/agents/providers").mock(return_value=httpx2.Response(200, json=[{}]))
        providers = Cloud(client).agents.providers.list()
        assert_matches_type(CloudAgentProviderList, providers, path=["response"])
        assert providers[0].name is None

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/agents/providers/primary").mock(
            return_value=httpx2.Response(200, json=PROVIDER)
        )
        provider = Cloud(client).agents.providers.retrieve("primary")
        assert_matches_type(CloudAgentProvider, provider, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/agents/providers").mock(return_value=httpx2.Response(200, json=[PROVIDER]))
        response = Cloud(client).agents.providers.with_raw_response.list()
        assert response.is_closed is True
        assert_matches_type(CloudAgentProviderList, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/agents/providers/primary").mock(
            return_value=httpx2.Response(200, json=PROVIDER)
        )
        with Cloud(client).agents.providers.with_streaming_response.retrieve("primary") as response:
            assert not response.is_closed
            assert_matches_type(CloudAgentProvider, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider_name` but received ''"):
            Cloud(client).agents.providers.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        _gate(respx_mock, client)
        route = respx_mock.get(url__regex=r".*providers.*").mock(return_value=httpx2.Response(200, json=PROVIDER))
        Cloud(client).agents.providers.retrieve("a b/c")
        assert "/apis/cloud.sn.io/v1/agents/providers/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.get(url__regex=r".*providers.*").mock(return_value=httpx2.Response(200, json=[PROVIDER]))
        with pytest.raises(ExtensionNotAvailableError):
            Cloud(client).agents.providers.list()
        assert route.called is False

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_gate_is_probed_once_per_client(self, client: Orca, respx_mock: MockRouter) -> None:
        """Discovery is cached, so a second gated call adds no second `GET /apis`."""
        apis = _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/agents/providers").mock(return_value=httpx2.Response(200, json=[PROVIDER]))
        providers = Cloud(client).agents.providers
        providers.list()
        providers.list()
        assert apis.call_count == 1


class TestAsyncProviders:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/agents/providers").mock(
            return_value=httpx2.Response(200, json=[PROVIDER])
        )
        providers = await AsyncCloud(async_client).agents.providers.list()
        assert_matches_type(CloudAgentProviderList, providers, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/agents/providers/primary").mock(
            return_value=httpx2.Response(200, json=PROVIDER)
        )
        provider = await AsyncCloud(async_client).agents.providers.retrieve("primary")
        assert_matches_type(CloudAgentProvider, provider, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/agents/providers").mock(return_value=httpx2.Response(200, json=[PROVIDER]))
        response = await AsyncCloud(async_client).agents.providers.with_raw_response.list()
        assert response.is_closed is True
        assert_matches_type(CloudAgentProviderList, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/agents/providers/primary").mock(
            return_value=httpx2.Response(200, json=PROVIDER)
        )
        async with AsyncCloud(async_client).agents.providers.with_streaming_response.retrieve("primary") as response:
            assert not response.is_closed
            assert_matches_type(CloudAgentProvider, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider_name` but received ''"):
            await AsyncCloud(async_client).agents.providers.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get(url__regex=r".*providers.*").mock(return_value=httpx2.Response(200, json=[PROVIDER]))
        with pytest.raises(ExtensionNotAvailableError):
            await AsyncCloud(async_client).agents.providers.list()
        assert route.called is False
