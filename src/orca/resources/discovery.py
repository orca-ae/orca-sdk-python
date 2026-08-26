from __future__ import annotations

import httpx2

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.api_group import APIGroupList

__all__ = ["Discovery", "AsyncDiscovery"]


class Discovery(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DiscoveryWithRawResponse:
        return DiscoveryWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DiscoveryWithStreamingResponse:
        return DiscoveryWithStreamingResponse(self)

    def groups(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> APIGroupList:
        """
        List the extension API groups this deployment serves.

        An empty `groups` list means "no extensions installed" on a deployment that
        supports discovery — not an error, and distinct from the 404 an older,
        pre-discovery deployment returns for this same call. Use it for your own
        capability checks: an extension namespace is callable only when its group
        name appears here.

        Note the path: `/apis` sits at the host root with no `/v1` prefix, because it
        describes the deployment rather than any one API version.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/apis",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIGroupList,
        )


class AsyncDiscovery(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDiscoveryWithRawResponse:
        return AsyncDiscoveryWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDiscoveryWithStreamingResponse:
        return AsyncDiscoveryWithStreamingResponse(self)

    async def groups(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> APIGroupList:
        """
        List the extension API groups this deployment serves.

        An empty `groups` list means "no extensions installed" on a deployment that
        supports discovery — not an error, and distinct from the 404 an older,
        pre-discovery deployment returns for this same call. Use it for your own
        capability checks: an extension namespace is callable only when its group
        name appears here.

        Note the path: `/apis` sits at the host root with no `/v1` prefix, because it
        describes the deployment rather than any one API version.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/apis",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIGroupList,
        )


class DiscoveryWithRawResponse:
    def __init__(self, discovery: Discovery) -> None:
        self._discovery = discovery

        self.groups = to_raw_response_wrapper(discovery.groups)


class AsyncDiscoveryWithRawResponse:
    def __init__(self, discovery: AsyncDiscovery) -> None:
        self._discovery = discovery

        self.groups = async_to_raw_response_wrapper(discovery.groups)


class DiscoveryWithStreamingResponse:
    def __init__(self, discovery: Discovery) -> None:
        self._discovery = discovery

        self.groups = to_streamed_response_wrapper(discovery.groups)


class AsyncDiscoveryWithStreamingResponse:
    def __init__(self, discovery: AsyncDiscovery) -> None:
        self._discovery = discovery

        self.groups = async_to_streamed_response_wrapper(discovery.groups)
