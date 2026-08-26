from __future__ import annotations

import httpx2

from .._gate import cloud_gate, async_cloud_gate
from ...._types import Body, Query, Headers, NotGiven, not_given
from ...._utils import path_template
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.cloud_agent_provider import CloudAgentProvider, CloudAgentProviderList

__all__ = ["Providers", "AsyncProviders"]


class Providers(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProvidersWithRawResponse:
        return ProvidersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProvidersWithStreamingResponse:
        return ProvidersWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudAgentProviderList:
        """
        List the model providers registered with this deployment.

        The whole registry comes back in one response; it is not paginated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/agents/providers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudAgentProviderList,
        )

    def retrieve(
        self,
        provider_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudAgentProvider:
        """
        Retrieve a single registered model provider.

        Args:
          provider_name: Registry name of the provider, as reported by `list()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not provider_name:
            raise ValueError(f"Expected a non-empty value for `provider_name` but received {provider_name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/agents/providers/{provider_name}", provider_name=provider_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudAgentProvider,
        )


class AsyncProviders(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProvidersWithRawResponse:
        return AsyncProvidersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProvidersWithStreamingResponse:
        return AsyncProvidersWithStreamingResponse(self)

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudAgentProviderList:
        """
        List the model providers registered with this deployment.

        The whole registry comes back in one response; it is not paginated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/agents/providers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudAgentProviderList,
        )

    async def retrieve(
        self,
        provider_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudAgentProvider:
        """
        Retrieve a single registered model provider.

        Args:
          provider_name: Registry name of the provider, as reported by `list()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not provider_name:
            raise ValueError(f"Expected a non-empty value for `provider_name` but received {provider_name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/agents/providers/{provider_name}", provider_name=provider_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudAgentProvider,
        )


class ProvidersWithRawResponse:
    def __init__(self, providers: Providers) -> None:
        self._providers = providers

        self.list = to_raw_response_wrapper(providers.list)
        self.retrieve = to_raw_response_wrapper(providers.retrieve)


class AsyncProvidersWithRawResponse:
    def __init__(self, providers: AsyncProviders) -> None:
        self._providers = providers

        self.list = async_to_raw_response_wrapper(providers.list)
        self.retrieve = async_to_raw_response_wrapper(providers.retrieve)


class ProvidersWithStreamingResponse:
    def __init__(self, providers: Providers) -> None:
        self._providers = providers

        self.list = to_streamed_response_wrapper(providers.list)
        self.retrieve = to_streamed_response_wrapper(providers.retrieve)


class AsyncProvidersWithStreamingResponse:
    def __init__(self, providers: AsyncProviders) -> None:
        self._providers = providers

        self.list = async_to_streamed_response_wrapper(providers.list)
        self.retrieve = async_to_streamed_response_wrapper(providers.retrieve)
