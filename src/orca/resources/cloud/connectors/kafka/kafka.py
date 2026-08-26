from __future__ import annotations

import httpx2

from ..._gate import cloud_gate, async_cloud_gate
from .plugins import (
    Plugins,
    AsyncPlugins,
    PluginsWithRawResponse,
    AsyncPluginsWithRawResponse,
    PluginsWithStreamingResponse,
    AsyncPluginsWithStreamingResponse,
)
from ....._types import Body, Query, Headers, NotGiven, not_given
from .connectors import (
    KafkaConnectors,
    AsyncKafkaConnectors,
    KafkaConnectorsWithRawResponse,
    AsyncKafkaConnectorsWithRawResponse,
    KafkaConnectorsWithStreamingResponse,
    AsyncKafkaConnectorsWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.cloud_kafka_shared import CloudKafkaServerInfo, CloudKafkaWorkerStatus

__all__ = ["Kafka", "AsyncKafka"]


class Kafka(SyncAPIResource):
    @cached_property
    def plugins(self) -> Plugins:
        return Plugins(self._client)

    @cached_property
    def connectors(self) -> KafkaConnectors:
        return KafkaConnectors(self._client)

    @cached_property
    def with_raw_response(self) -> KafkaWithRawResponse:
        return KafkaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KafkaWithStreamingResponse:
        return KafkaWithStreamingResponse(self)

    def health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaWorkerStatus:
        """
        Check the connect worker's health.

        This reports on the worker process, not on any connector it runs: a healthy
        worker can still be hosting a failed connector.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/connectors/kafka/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaWorkerStatus,
        )

    def server_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaServerInfo:
        """
        Retrieve the connect worker's version and cluster identity.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/connectors/kafka",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaServerInfo,
        )


class AsyncKafka(AsyncAPIResource):
    @cached_property
    def plugins(self) -> AsyncPlugins:
        return AsyncPlugins(self._client)

    @cached_property
    def connectors(self) -> AsyncKafkaConnectors:
        return AsyncKafkaConnectors(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncKafkaWithRawResponse:
        return AsyncKafkaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKafkaWithStreamingResponse:
        return AsyncKafkaWithStreamingResponse(self)

    async def health(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaWorkerStatus:
        """
        Check the connect worker's health.

        This reports on the worker process, not on any connector it runs: a healthy
        worker can still be hosting a failed connector.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/connectors/kafka/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaWorkerStatus,
        )

    async def server_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaServerInfo:
        """
        Retrieve the connect worker's version and cluster identity.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/connectors/kafka",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaServerInfo,
        )


class KafkaWithRawResponse:
    def __init__(self, kafka: Kafka) -> None:
        self._kafka = kafka

        self.health = to_raw_response_wrapper(kafka.health)
        self.server_info = to_raw_response_wrapper(kafka.server_info)

    @cached_property
    def plugins(self) -> PluginsWithRawResponse:
        return PluginsWithRawResponse(self._kafka.plugins)

    @cached_property
    def connectors(self) -> KafkaConnectorsWithRawResponse:
        return KafkaConnectorsWithRawResponse(self._kafka.connectors)


class AsyncKafkaWithRawResponse:
    def __init__(self, kafka: AsyncKafka) -> None:
        self._kafka = kafka

        self.health = async_to_raw_response_wrapper(kafka.health)
        self.server_info = async_to_raw_response_wrapper(kafka.server_info)

    @cached_property
    def plugins(self) -> AsyncPluginsWithRawResponse:
        return AsyncPluginsWithRawResponse(self._kafka.plugins)

    @cached_property
    def connectors(self) -> AsyncKafkaConnectorsWithRawResponse:
        return AsyncKafkaConnectorsWithRawResponse(self._kafka.connectors)


class KafkaWithStreamingResponse:
    def __init__(self, kafka: Kafka) -> None:
        self._kafka = kafka

        self.health = to_streamed_response_wrapper(kafka.health)
        self.server_info = to_streamed_response_wrapper(kafka.server_info)

    @cached_property
    def plugins(self) -> PluginsWithStreamingResponse:
        return PluginsWithStreamingResponse(self._kafka.plugins)

    @cached_property
    def connectors(self) -> KafkaConnectorsWithStreamingResponse:
        return KafkaConnectorsWithStreamingResponse(self._kafka.connectors)


class AsyncKafkaWithStreamingResponse:
    def __init__(self, kafka: AsyncKafka) -> None:
        self._kafka = kafka

        self.health = async_to_streamed_response_wrapper(kafka.health)
        self.server_info = async_to_streamed_response_wrapper(kafka.server_info)

    @cached_property
    def plugins(self) -> AsyncPluginsWithStreamingResponse:
        return AsyncPluginsWithStreamingResponse(self._kafka.plugins)

    @cached_property
    def connectors(self) -> AsyncKafkaConnectorsWithStreamingResponse:
        return AsyncKafkaConnectorsWithStreamingResponse(self._kafka.connectors)
