from __future__ import annotations

from .kafka import (
    Kafka,
    AsyncKafka,
    KafkaWithRawResponse,
    AsyncKafkaWithRawResponse,
    KafkaWithStreamingResponse,
    AsyncKafkaWithStreamingResponse,
)
from .sinks import (
    SinkConnectors,
    AsyncSinkConnectors,
    SinkConnectorsWithRawResponse,
    AsyncSinkConnectorsWithRawResponse,
    SinkConnectorsWithStreamingResponse,
    AsyncSinkConnectorsWithStreamingResponse,
)
from .sources import (
    SourceConnectors,
    AsyncSourceConnectors,
    SourceConnectorsWithRawResponse,
    AsyncSourceConnectorsWithRawResponse,
    SourceConnectorsWithStreamingResponse,
    AsyncSourceConnectorsWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Connectors", "AsyncConnectors"]


class Connectors(SyncAPIResource):
    """Router over the three connector runtimes this deployment serves.

    It holds no operations of its own: `sinks` and `sources` are the connector
    registry, and `kafka` is the separate connect worker with its own protocol.
    """

    @cached_property
    def sinks(self) -> SinkConnectors:
        return SinkConnectors(self._client)

    @cached_property
    def sources(self) -> SourceConnectors:
        return SourceConnectors(self._client)

    @cached_property
    def kafka(self) -> Kafka:
        return Kafka(self._client)

    @cached_property
    def with_raw_response(self) -> ConnectorsWithRawResponse:
        return ConnectorsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConnectorsWithStreamingResponse:
        return ConnectorsWithStreamingResponse(self)


class AsyncConnectors(AsyncAPIResource):
    """Router over the three connector runtimes this deployment serves.

    It holds no operations of its own: `sinks` and `sources` are the connector
    registry, and `kafka` is the separate connect worker with its own protocol.
    """

    @cached_property
    def sinks(self) -> AsyncSinkConnectors:
        return AsyncSinkConnectors(self._client)

    @cached_property
    def sources(self) -> AsyncSourceConnectors:
        return AsyncSourceConnectors(self._client)

    @cached_property
    def kafka(self) -> AsyncKafka:
        return AsyncKafka(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConnectorsWithRawResponse:
        return AsyncConnectorsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConnectorsWithStreamingResponse:
        return AsyncConnectorsWithStreamingResponse(self)


class ConnectorsWithRawResponse:
    def __init__(self, connectors: Connectors) -> None:
        self._connectors = connectors

    @cached_property
    def sinks(self) -> SinkConnectorsWithRawResponse:
        return SinkConnectorsWithRawResponse(self._connectors.sinks)

    @cached_property
    def sources(self) -> SourceConnectorsWithRawResponse:
        return SourceConnectorsWithRawResponse(self._connectors.sources)

    @cached_property
    def kafka(self) -> KafkaWithRawResponse:
        return KafkaWithRawResponse(self._connectors.kafka)


class AsyncConnectorsWithRawResponse:
    def __init__(self, connectors: AsyncConnectors) -> None:
        self._connectors = connectors

    @cached_property
    def sinks(self) -> AsyncSinkConnectorsWithRawResponse:
        return AsyncSinkConnectorsWithRawResponse(self._connectors.sinks)

    @cached_property
    def sources(self) -> AsyncSourceConnectorsWithRawResponse:
        return AsyncSourceConnectorsWithRawResponse(self._connectors.sources)

    @cached_property
    def kafka(self) -> AsyncKafkaWithRawResponse:
        return AsyncKafkaWithRawResponse(self._connectors.kafka)


class ConnectorsWithStreamingResponse:
    def __init__(self, connectors: Connectors) -> None:
        self._connectors = connectors

    @cached_property
    def sinks(self) -> SinkConnectorsWithStreamingResponse:
        return SinkConnectorsWithStreamingResponse(self._connectors.sinks)

    @cached_property
    def sources(self) -> SourceConnectorsWithStreamingResponse:
        return SourceConnectorsWithStreamingResponse(self._connectors.sources)

    @cached_property
    def kafka(self) -> KafkaWithStreamingResponse:
        return KafkaWithStreamingResponse(self._connectors.kafka)


class AsyncConnectorsWithStreamingResponse:
    def __init__(self, connectors: AsyncConnectors) -> None:
        self._connectors = connectors

    @cached_property
    def sinks(self) -> AsyncSinkConnectorsWithStreamingResponse:
        return AsyncSinkConnectorsWithStreamingResponse(self._connectors.sinks)

    @cached_property
    def sources(self) -> AsyncSourceConnectorsWithStreamingResponse:
        return AsyncSourceConnectorsWithStreamingResponse(self._connectors.sources)

    @cached_property
    def kafka(self) -> AsyncKafkaWithStreamingResponse:
        return AsyncKafkaWithStreamingResponse(self._connectors.kafka)
