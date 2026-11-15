# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import httpx2

from ...types import model_price_rule_list_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._constants import PRICING_EXTENSION_GROUP
from ...pagination import SyncModelPriceRulePage, AsyncModelPriceRulePage
from ..._base_client import AsyncPaginator, make_request_options
from .._extension_gate import extension_gate, async_extension_gate
from ...types.model_price_rule import ModelPriceRule

__all__ = ["ModelPriceRules", "AsyncModelPriceRules"]


class ModelPriceRules(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ModelPriceRulesWithRawResponse:
        return ModelPriceRulesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelPriceRulesWithStreamingResponse:
        return ModelPriceRulesWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncModelPriceRulePage[ModelPriceRule]:
        """List engine pricing rules; expired catalog cursors raise 410 without restarting.

        Args:
          limit: Maximum number of rules per page (1 to 100).
          page: Opaque cursor from the previous catalog page.
          extra_headers: Send extra headers
          extra_query: Add additional query parameters to the request
          extra_body: Add additional JSON properties to the request
          timeout: Override the client-level default timeout for this request, in seconds
        """
        extension_gate(self, PRICING_EXTENSION_GROUP, "v2")
        return self._get_api_list(
            "/apis/pricing.runorca.ai/v2/modelpricerules",
            page=SyncModelPriceRulePage[ModelPriceRule],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    model_price_rule_list_params.ModelPriceRuleListParams,
                ),
            ),
            model=ModelPriceRule,
        )


class AsyncModelPriceRules(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncModelPriceRulesWithRawResponse:
        return AsyncModelPriceRulesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelPriceRulesWithStreamingResponse:
        return AsyncModelPriceRulesWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ModelPriceRule, AsyncModelPriceRulePage[ModelPriceRule]]:
        """List engine pricing rules; expired catalog cursors raise 410 without restarting.

        Args:
          limit: Maximum number of rules per page (1 to 100).
          page: Opaque cursor from the previous catalog page.
          extra_headers: Send extra headers
          extra_query: Add additional query parameters to the request
          extra_body: Add additional JSON properties to the request
          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/apis/pricing.runorca.ai/v2/modelpricerules",
            page=AsyncModelPriceRulePage[ModelPriceRule],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    model_price_rule_list_params.ModelPriceRuleListParams,
                ),
            ),
            model=ModelPriceRule,
            pre_request=lambda: async_extension_gate(self, PRICING_EXTENSION_GROUP, "v2"),
        )


class ModelPriceRulesWithRawResponse:
    def __init__(self, model_price_rules: ModelPriceRules) -> None:
        self._model_price_rules = model_price_rules
        self.list = to_raw_response_wrapper(model_price_rules.list)


class AsyncModelPriceRulesWithRawResponse:
    def __init__(self, model_price_rules: AsyncModelPriceRules) -> None:
        self._model_price_rules = model_price_rules
        self.list = async_to_raw_response_wrapper(model_price_rules.list)


class ModelPriceRulesWithStreamingResponse:
    def __init__(self, model_price_rules: ModelPriceRules) -> None:
        self._model_price_rules = model_price_rules
        self.list = to_streamed_response_wrapper(model_price_rules.list)


class AsyncModelPriceRulesWithStreamingResponse:
    def __init__(self, model_price_rules: AsyncModelPriceRules) -> None:
        self._model_price_rules = model_price_rules
        self.list = async_to_streamed_response_wrapper(model_price_rules.list)
