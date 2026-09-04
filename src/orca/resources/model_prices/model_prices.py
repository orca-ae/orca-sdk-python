from __future__ import annotations

import httpx2

from ...types import model_price_list_params, model_price_retrieve_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._constants import PRICING_EXTENSION_GROUP
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from .._extension_gate import extension_gate, async_extension_gate
from ...types.model_price import ModelPrice

__all__ = ["ModelPrices", "AsyncModelPrices"]


class ModelPrices(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ModelPricesWithRawResponse:
        return ModelPricesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelPricesWithStreamingResponse:
        return ModelPricesWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[ModelPrice]:
        """List the effective model prices used for cost accounting."""
        extension_gate(self, PRICING_EXTENSION_GROUP)
        return self._get_api_list(
            "/apis/pricing.runorca.ai/v1/modelprices",
            page=SyncPageCursor[ModelPrice],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    model_price_list_params.ModelPriceListParams,
                ),
            ),
            model=ModelPrice,
        )

    def retrieve(
        self,
        model_id: str,
        *,
        provider: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ModelPrice:
        """Retrieve the effective price for a model and optional provider."""
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        extension_gate(self, PRICING_EXTENSION_GROUP)
        return self._get(
            path_template("/apis/pricing.runorca.ai/v1/modelprices/{model_id}", model_id=model_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"provider": provider},
                    model_price_retrieve_params.ModelPriceRetrieveParams,
                ),
            ),
            cast_to=ModelPrice,
        )


class AsyncModelPrices(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncModelPricesWithRawResponse:
        return AsyncModelPricesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelPricesWithStreamingResponse:
        return AsyncModelPricesWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ModelPrice, AsyncPageCursor[ModelPrice]]:
        """List the effective model prices used for cost accounting."""
        return self._get_api_list(
            "/apis/pricing.runorca.ai/v1/modelprices",
            page=AsyncPageCursor[ModelPrice],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    model_price_list_params.ModelPriceListParams,
                ),
            ),
            model=ModelPrice,
            pre_request=lambda: async_extension_gate(self, PRICING_EXTENSION_GROUP),
        )

    async def retrieve(
        self,
        model_id: str,
        *,
        provider: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ModelPrice:
        """Retrieve the effective price for a model and optional provider."""
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        await async_extension_gate(self, PRICING_EXTENSION_GROUP)
        return await self._get(
            path_template("/apis/pricing.runorca.ai/v1/modelprices/{model_id}", model_id=model_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"provider": provider},
                    model_price_retrieve_params.ModelPriceRetrieveParams,
                ),
            ),
            cast_to=ModelPrice,
        )


class ModelPricesWithRawResponse:
    def __init__(self, model_prices: ModelPrices) -> None:
        self._model_prices = model_prices
        self.list = to_raw_response_wrapper(model_prices.list)
        self.retrieve = to_raw_response_wrapper(model_prices.retrieve)


class AsyncModelPricesWithRawResponse:
    def __init__(self, model_prices: AsyncModelPrices) -> None:
        self._model_prices = model_prices
        self.list = async_to_raw_response_wrapper(model_prices.list)
        self.retrieve = async_to_raw_response_wrapper(model_prices.retrieve)


class ModelPricesWithStreamingResponse:
    def __init__(self, model_prices: ModelPrices) -> None:
        self._model_prices = model_prices
        self.list = to_streamed_response_wrapper(model_prices.list)
        self.retrieve = to_streamed_response_wrapper(model_prices.retrieve)


class AsyncModelPricesWithStreamingResponse:
    def __init__(self, model_prices: AsyncModelPrices) -> None:
        self._model_prices = model_prices
        self.list = async_to_streamed_response_wrapper(model_prices.list)
        self.retrieve = async_to_streamed_response_wrapper(model_prices.retrieve)
