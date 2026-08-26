from __future__ import annotations

import httpx2

from ._gate import cloud_gate, async_cloud_gate
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.cloud_api_resource import CloudAPIResourceList

__all__ = ["APIResources", "AsyncAPIResources"]


class APIResources(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> APIResourcesWithRawResponse:
        return APIResourcesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIResourcesWithStreamingResponse:
        return APIResourcesWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudAPIResourceList:
        """
        List the resources the cloud extension API group advertises.

        The trailing slash is part of the route: the group root is `.../v1/`, not
        `.../v1`. This returns the whole listing in one response -- the group root is
        not a paginated collection.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudAPIResourceList,
        )


class AsyncAPIResources(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAPIResourcesWithRawResponse:
        return AsyncAPIResourcesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIResourcesWithStreamingResponse:
        return AsyncAPIResourcesWithStreamingResponse(self)

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudAPIResourceList:
        """
        List the resources the cloud extension API group advertises.

        The trailing slash is part of the route: the group root is `.../v1/`, not
        `.../v1`. This returns the whole listing in one response -- the group root is
        not a paginated collection.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudAPIResourceList,
        )


class APIResourcesWithRawResponse:
    def __init__(self, api_resources: APIResources) -> None:
        self._api_resources = api_resources

        self.list = to_raw_response_wrapper(api_resources.list)


class AsyncAPIResourcesWithRawResponse:
    def __init__(self, api_resources: AsyncAPIResources) -> None:
        self._api_resources = api_resources

        self.list = async_to_raw_response_wrapper(api_resources.list)


class APIResourcesWithStreamingResponse:
    def __init__(self, api_resources: APIResources) -> None:
        self._api_resources = api_resources

        self.list = to_streamed_response_wrapper(api_resources.list)


class AsyncAPIResourcesWithStreamingResponse:
    def __init__(self, api_resources: AsyncAPIResources) -> None:
        self._api_resources = api_resources

        self.list = async_to_streamed_response_wrapper(api_resources.list)
