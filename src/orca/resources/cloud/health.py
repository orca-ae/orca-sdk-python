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

__all__ = ["Health", "AsyncHealth"]


class Health(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HealthWithRawResponse:
        return HealthWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HealthWithStreamingResponse:
        return HealthWithStreamingResponse(self)

    def check(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> bool:
        """
        Check the cloud extension service health.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=bool,
        )

    def ready(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> bool:
        """
        Check whether the cloud extension service is ready.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/health/ready",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=bool,
        )

    def live(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> bool:
        """
        Check whether the cloud extension service is live.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/health/live",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=bool,
        )


class AsyncHealth(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHealthWithRawResponse:
        return AsyncHealthWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHealthWithStreamingResponse:
        return AsyncHealthWithStreamingResponse(self)

    async def check(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> bool:
        """
        Check the cloud extension service health.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=bool,
        )

    async def ready(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> bool:
        """
        Check whether the cloud extension service is ready.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/health/ready",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=bool,
        )

    async def live(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> bool:
        """
        Check whether the cloud extension service is live.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/health/live",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=bool,
        )


class HealthWithRawResponse:
    def __init__(self, health: Health) -> None:
        self._health = health

        self.check = to_raw_response_wrapper(health.check)
        self.ready = to_raw_response_wrapper(health.ready)
        self.live = to_raw_response_wrapper(health.live)


class AsyncHealthWithRawResponse:
    def __init__(self, health: AsyncHealth) -> None:
        self._health = health

        self.check = async_to_raw_response_wrapper(health.check)
        self.ready = async_to_raw_response_wrapper(health.ready)
        self.live = async_to_raw_response_wrapper(health.live)


class HealthWithStreamingResponse:
    def __init__(self, health: Health) -> None:
        self._health = health

        self.check = to_streamed_response_wrapper(health.check)
        self.ready = to_streamed_response_wrapper(health.ready)
        self.live = to_streamed_response_wrapper(health.live)


class AsyncHealthWithStreamingResponse:
    def __init__(self, health: AsyncHealth) -> None:
        self._health = health

        self.check = async_to_streamed_response_wrapper(health.check)
        self.ready = async_to_streamed_response_wrapper(health.ready)
        self.live = async_to_streamed_response_wrapper(health.live)
