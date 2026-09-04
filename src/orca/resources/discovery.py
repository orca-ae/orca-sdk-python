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
from .._constants import POLICY_EXTENSION_GROUP, PRICING_EXTENSION_GROUP
from .._base_client import make_request_options
from ._extension_gate import extension_gate, async_extension_gate
from ..types.api_group import APIGroupList
from ..types.api_resource import APIResourceList

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

    def policy_group_resources(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> APIResourceList:
        """List resources advertised by the policy extension API group."""
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._get(
            "/apis/policy.runorca.ai/v1",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResourceList,
        )

    def pricing_group_resources(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> APIResourceList:
        """List resources advertised by the pricing extension API group."""
        extension_gate(self, PRICING_EXTENSION_GROUP)
        return self._get(
            "/apis/pricing.runorca.ai/v1",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResourceList,
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

    async def policy_group_resources(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> APIResourceList:
        """List resources advertised by the policy extension API group."""
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._get(
            "/apis/policy.runorca.ai/v1",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResourceList,
        )

    async def pricing_group_resources(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> APIResourceList:
        """List resources advertised by the pricing extension API group."""
        await async_extension_gate(self, PRICING_EXTENSION_GROUP)
        return await self._get(
            "/apis/pricing.runorca.ai/v1",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResourceList,
        )


class DiscoveryWithRawResponse:
    def __init__(self, discovery: Discovery) -> None:
        self._discovery = discovery

        self.groups = to_raw_response_wrapper(discovery.groups)
        self.policy_group_resources = to_raw_response_wrapper(discovery.policy_group_resources)
        self.pricing_group_resources = to_raw_response_wrapper(discovery.pricing_group_resources)


class AsyncDiscoveryWithRawResponse:
    def __init__(self, discovery: AsyncDiscovery) -> None:
        self._discovery = discovery

        self.groups = async_to_raw_response_wrapper(discovery.groups)
        self.policy_group_resources = async_to_raw_response_wrapper(discovery.policy_group_resources)
        self.pricing_group_resources = async_to_raw_response_wrapper(discovery.pricing_group_resources)


class DiscoveryWithStreamingResponse:
    def __init__(self, discovery: Discovery) -> None:
        self._discovery = discovery

        self.groups = to_streamed_response_wrapper(discovery.groups)
        self.policy_group_resources = to_streamed_response_wrapper(discovery.policy_group_resources)
        self.pricing_group_resources = to_streamed_response_wrapper(discovery.pricing_group_resources)


class AsyncDiscoveryWithStreamingResponse:
    def __init__(self, discovery: AsyncDiscovery) -> None:
        self._discovery = discovery

        self.groups = async_to_streamed_response_wrapper(discovery.groups)
        self.policy_group_resources = async_to_streamed_response_wrapper(discovery.policy_group_resources)
        self.pricing_group_resources = async_to_streamed_response_wrapper(discovery.pricing_group_resources)
