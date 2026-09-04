from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from orca.types import ModelPrice
from tests.utils import assert_matches_type
from orca.pagination import SyncPageCursor, AsyncPageCursor

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

MODEL_PRICE: dict[str, Any] = {
    "type": "model_price",
    "provider": "provider-a",
    "model_id": "model-alpha",
    "input_per_million_tokens": 3,
    "output_per_million_tokens": 15,
    "cache_read_per_million_tokens": 0.3,
    "cache_write_per_million_tokens": 3.75,
}


def _req(route: Any) -> httpx2.Request:
    return cast("httpx2.Request", route.calls[0].request)


def _gate(respx_mock: MockRouter, client: Orca | AsyncOrca, *, available: bool = True) -> Any:
    client._extension_groups.clear()
    groups = [{"name": "pricing.runorca.ai"}] if available else []
    return respx_mock.get("/apis").mock(
        return_value=httpx2.Response(200, json={"kind": "APIGroupList", "groups": groups})
    )


class TestModelPrices:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_with_pagination(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/pricing.runorca.ai/v1/modelprices").mock(
            return_value=httpx2.Response(200, json={"data": [MODEL_PRICE], "next_page": None})
        )
        page = client.model_prices.list(limit=10, page="next")
        assert_matches_type(SyncPageCursor[ModelPrice], page, path=["response"])
        assert _req(route).url.params["limit"] == "10"
        assert _req(route).url.params["page"] == "next"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_escapes_model_id_and_qualifies_provider(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(url__regex=r".*/apis/pricing\.runorca\.ai/v1/modelprices/.*").mock(
            return_value=httpx2.Response(200, json=MODEL_PRICE)
        )
        result = client.model_prices.retrieve("model/alpha", provider="provider-a", extra_headers={"X-Test": "get"})
        assert_matches_type(ModelPrice, result, path=["response"])
        assert str(_req(route).url).split("?", 1)[0].endswith("/modelprices/model%2Falpha")
        assert _req(route).url.params["provider"] == "provider-a"
        assert _req(route).headers["x-test"] == "get"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_and_streaming_wrappers(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/pricing.runorca.ai/v1/modelprices/model-alpha").mock(
            return_value=httpx2.Response(200, json=MODEL_PRICE)
        )
        raw = client.model_prices.with_raw_response.retrieve("model-alpha")
        assert_matches_type(ModelPrice, raw.parse(), path=["response"])
        with client.model_prices.with_streaming_response.retrieve("model-alpha") as streamed:
            assert_matches_type(ModelPrice, streamed.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_before_business_request(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client, available=False)
        route = respx_mock.get("/apis/pricing.runorca.ai/v1/modelprices/model-alpha").mock(
            return_value=httpx2.Response(200, json=MODEL_PRICE)
        )
        with pytest.raises(ExtensionNotAvailableError, match="pricing.runorca.ai"):
            client.model_prices.retrieve("model-alpha")
        assert route.called is False


class TestAsyncModelPrices:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_and_paginated_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/pricing.runorca.ai/v1/modelprices/model-alpha").mock(
            return_value=httpx2.Response(200, json=MODEL_PRICE)
        )
        result = await async_client.model_prices.retrieve("model-alpha")
        assert_matches_type(ModelPrice, result, path=["response"])

        respx_mock.get("/apis/pricing.runorca.ai/v1/modelprices").mock(
            return_value=httpx2.Response(200, json={"data": [MODEL_PRICE], "next_page": None})
        )
        page = await async_client.model_prices.list()
        assert_matches_type(AsyncPageCursor[ModelPrice], page, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_paginated_raw_and_streaming_wrappers(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/pricing.runorca.ai/v1/modelprices").mock(
            return_value=httpx2.Response(200, json={"data": [MODEL_PRICE], "next_page": None})
        )
        raw = await async_client.model_prices.with_raw_response.list()
        assert_matches_type(AsyncPageCursor[ModelPrice], await raw.parse(), path=["response"])
        async with async_client.model_prices.with_streaming_response.list() as streamed:
            assert_matches_type(AsyncPageCursor[ModelPrice], await streamed.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_paginated_list_is_gated_before_request(
        self, async_client: AsyncOrca, respx_mock: MockRouter
    ) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get("/apis/pricing.runorca.ai/v1/modelprices").mock(
            return_value=httpx2.Response(200, json={"data": [], "next_page": None})
        )
        with pytest.raises(ExtensionNotAvailableError, match="pricing.runorca.ai"):
            await async_client.model_prices.list()
        assert route.called is False
