from __future__ import annotations

import os
from typing import Any, Union, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.resources.cloud import Cloud, AsyncCloud
from orca.types.cloud_catalog import CloudCatalogConnectorList, CloudCatalogConfigFieldList
from orca.resources.cloud.catalog import (
    SinkCatalog,
    KafkaCatalog,
    SourceCatalog,
    AsyncSinkCatalog,
    AsyncKafkaCatalog,
    AsyncSourceCatalog,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

# camelCase because the catalog serves these fields that way; the SDK mirrors the
# wire shape rather than renaming it.
CONNECTORS: list[dict[str, Any]] = [
    {
        "name": "jdbc",
        "description": "Relational database connector",
        "sourceClass": "io.example.JdbcSource",
        "sinkClass": "io.example.JdbcSink",
        "sourceConfigClass": "io.example.JdbcSourceConfig",
        "sinkConfigClass": "io.example.JdbcSinkConfig",
    }
]

CONFIG_FIELDS: list[dict[str, Any]] = [
    {"fieldName": "url", "typeName": "java.lang.String", "attributes": {"required": "true"}}
]

FAMILIES = pytest.mark.parametrize("family", ["kafka", "sinks", "sources"])

SyncFamily = Union[KafkaCatalog, SinkCatalog, SourceCatalog]
AsyncFamily = Union[AsyncKafkaCatalog, AsyncSinkCatalog, AsyncSourceCatalog]


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


def _sync_family(client: Orca, family: str) -> SyncFamily:
    """Resolve a family name to its resource through the real router chain."""
    catalog = Cloud(client).catalog
    if family == "kafka":
        return catalog.kafka
    if family == "sinks":
        return catalog.sinks
    return catalog.sources


def _async_family(client: AsyncOrca, family: str) -> AsyncFamily:
    catalog = AsyncCloud(client).catalog
    if family == "kafka":
        return catalog.kafka
    if family == "sinks":
        return catalog.sinks
    return catalog.sources


class TestCatalog:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter, family: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}").mock(
            return_value=httpx2.Response(200, json=CONNECTORS)
        )
        connectors = _sync_family(client, family).list()
        assert_matches_type(CloudCatalogConnectorList, connectors, path=["response"])
        assert _req(route).method == "GET"
        assert connectors[0].sourceClass == "io.example.JdbcSource"

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter, family: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}/jdbc").mock(
            return_value=httpx2.Response(200, json=CONFIG_FIELDS)
        )
        fields = _sync_family(client, family).retrieve("jdbc")
        assert_matches_type(CloudCatalogConfigFieldList, fields, path=["response"])
        assert _req(route).method == "GET"
        assert fields[0].fieldName == "url"
        assert fields[0].attributes == {"required": "true"}

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: Orca, respx_mock: MockRouter, family: str) -> None:
        _gate(respx_mock, client)
        respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}").mock(
            return_value=httpx2.Response(200, json=CONNECTORS)
        )
        response = _sync_family(client, family).with_raw_response.list()
        assert response.is_closed is True
        assert_matches_type(CloudCatalogConnectorList, response.parse(), path=["response"])

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: Orca, respx_mock: MockRouter, family: str) -> None:
        _gate(respx_mock, client)
        respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}/jdbc").mock(
            return_value=httpx2.Response(200, json=CONFIG_FIELDS)
        )
        with _sync_family(client, family).with_streaming_response.retrieve("jdbc") as response:
            assert not response.is_closed
            assert_matches_type(CloudCatalogConfigFieldList, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            Cloud(client).catalog.kafka.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        _gate(respx_mock, client)
        route = respx_mock.get(url__regex=r".*catalog.*").mock(return_value=httpx2.Response(200, json=CONFIG_FIELDS))
        Cloud(client).catalog.sinks.retrieve("a b/c")
        assert "/apis/cloud.sn.io/v1/catalog/sinks/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.get(url__regex=r".*catalog.*").mock(return_value=httpx2.Response(200, json=CONNECTORS))
        with pytest.raises(ExtensionNotAvailableError):
            Cloud(client).catalog.kafka.list()
        assert route.called is False

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_retrieve_before_path_validation(self, client: Orca, respx_mock: MockRouter) -> None:
        """The gate runs first, so an unavailable namespace outranks a bad path param."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.get(url__regex=r".*catalog.*").mock(return_value=httpx2.Response(200, json=CONFIG_FIELDS))
        with pytest.raises(ExtensionNotAvailableError):
            Cloud(client).catalog.sources.retrieve("")
        assert route.called is False


class TestAsyncCatalog:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter, family: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}").mock(
            return_value=httpx2.Response(200, json=CONNECTORS)
        )
        connectors = await _async_family(async_client, family).list()
        assert_matches_type(CloudCatalogConnectorList, connectors, path=["response"])
        assert _req(route).method == "GET"

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter, family: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}/jdbc").mock(
            return_value=httpx2.Response(200, json=CONFIG_FIELDS)
        )
        fields = await _async_family(async_client, family).retrieve("jdbc")
        assert_matches_type(CloudCatalogConfigFieldList, fields, path=["response"])
        assert _req(route).method == "GET"

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncOrca, respx_mock: MockRouter, family: str) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}").mock(
            return_value=httpx2.Response(200, json=CONNECTORS)
        )
        response = await _async_family(async_client, family).with_raw_response.list()
        assert response.is_closed is True
        assert_matches_type(CloudCatalogConnectorList, await response.parse(), path=["response"])

    @FAMILIES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(
        self, async_client: AsyncOrca, respx_mock: MockRouter, family: str
    ) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get(f"/apis/cloud.sn.io/v1/catalog/{family}/jdbc").mock(
            return_value=httpx2.Response(200, json=CONFIG_FIELDS)
        )
        async with _async_family(async_client, family).with_streaming_response.retrieve("jdbc") as response:
            assert not response.is_closed
            assert_matches_type(CloudCatalogConfigFieldList, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await AsyncCloud(async_client).catalog.kafka.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_is_escaped(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(url__regex=r".*catalog.*").mock(return_value=httpx2.Response(200, json=CONFIG_FIELDS))
        await AsyncCloud(async_client).catalog.sinks.retrieve("a b/c")
        assert "/apis/cloud.sn.io/v1/catalog/sinks/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get(url__regex=r".*catalog.*").mock(return_value=httpx2.Response(200, json=CONNECTORS))
        with pytest.raises(ExtensionNotAvailableError):
            await AsyncCloud(async_client).catalog.kafka.list()
        assert route.called is False
