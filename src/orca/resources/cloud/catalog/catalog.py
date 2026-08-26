from __future__ import annotations

from .kafka import (
    KafkaCatalog,
    AsyncKafkaCatalog,
    KafkaCatalogWithRawResponse,
    AsyncKafkaCatalogWithRawResponse,
    KafkaCatalogWithStreamingResponse,
    AsyncKafkaCatalogWithStreamingResponse,
)
from .sinks import (
    SinkCatalog,
    AsyncSinkCatalog,
    SinkCatalogWithRawResponse,
    AsyncSinkCatalogWithRawResponse,
    SinkCatalogWithStreamingResponse,
    AsyncSinkCatalogWithStreamingResponse,
)
from .sources import (
    SourceCatalog,
    AsyncSourceCatalog,
    SourceCatalogWithRawResponse,
    AsyncSourceCatalogWithRawResponse,
    SourceCatalogWithStreamingResponse,
    AsyncSourceCatalogWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Catalog", "AsyncCatalog"]


class Catalog(SyncAPIResource):
    """Read-only connector catalogs.

    A router only: the catalog itself is served per connector family, so every
    request goes through `kafka`, `sinks`, or `sources`.
    """

    @cached_property
    def kafka(self) -> KafkaCatalog:
        return KafkaCatalog(self._client)

    @cached_property
    def sinks(self) -> SinkCatalog:
        return SinkCatalog(self._client)

    @cached_property
    def sources(self) -> SourceCatalog:
        return SourceCatalog(self._client)

    @cached_property
    def with_raw_response(self) -> CatalogWithRawResponse:
        return CatalogWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CatalogWithStreamingResponse:
        return CatalogWithStreamingResponse(self)


class AsyncCatalog(AsyncAPIResource):
    """Read-only connector catalogs.

    A router only: the catalog itself is served per connector family, so every
    request goes through `kafka`, `sinks`, or `sources`.
    """

    @cached_property
    def kafka(self) -> AsyncKafkaCatalog:
        return AsyncKafkaCatalog(self._client)

    @cached_property
    def sinks(self) -> AsyncSinkCatalog:
        return AsyncSinkCatalog(self._client)

    @cached_property
    def sources(self) -> AsyncSourceCatalog:
        return AsyncSourceCatalog(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCatalogWithRawResponse:
        return AsyncCatalogWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCatalogWithStreamingResponse:
        return AsyncCatalogWithStreamingResponse(self)


class CatalogWithRawResponse:
    def __init__(self, catalog: Catalog) -> None:
        self._catalog = catalog

    @cached_property
    def kafka(self) -> KafkaCatalogWithRawResponse:
        return KafkaCatalogWithRawResponse(self._catalog.kafka)

    @cached_property
    def sinks(self) -> SinkCatalogWithRawResponse:
        return SinkCatalogWithRawResponse(self._catalog.sinks)

    @cached_property
    def sources(self) -> SourceCatalogWithRawResponse:
        return SourceCatalogWithRawResponse(self._catalog.sources)


class AsyncCatalogWithRawResponse:
    def __init__(self, catalog: AsyncCatalog) -> None:
        self._catalog = catalog

    @cached_property
    def kafka(self) -> AsyncKafkaCatalogWithRawResponse:
        return AsyncKafkaCatalogWithRawResponse(self._catalog.kafka)

    @cached_property
    def sinks(self) -> AsyncSinkCatalogWithRawResponse:
        return AsyncSinkCatalogWithRawResponse(self._catalog.sinks)

    @cached_property
    def sources(self) -> AsyncSourceCatalogWithRawResponse:
        return AsyncSourceCatalogWithRawResponse(self._catalog.sources)


class CatalogWithStreamingResponse:
    def __init__(self, catalog: Catalog) -> None:
        self._catalog = catalog

    @cached_property
    def kafka(self) -> KafkaCatalogWithStreamingResponse:
        return KafkaCatalogWithStreamingResponse(self._catalog.kafka)

    @cached_property
    def sinks(self) -> SinkCatalogWithStreamingResponse:
        return SinkCatalogWithStreamingResponse(self._catalog.sinks)

    @cached_property
    def sources(self) -> SourceCatalogWithStreamingResponse:
        return SourceCatalogWithStreamingResponse(self._catalog.sources)


class AsyncCatalogWithStreamingResponse:
    def __init__(self, catalog: AsyncCatalog) -> None:
        self._catalog = catalog

    @cached_property
    def kafka(self) -> AsyncKafkaCatalogWithStreamingResponse:
        return AsyncKafkaCatalogWithStreamingResponse(self._catalog.kafka)

    @cached_property
    def sinks(self) -> AsyncSinkCatalogWithStreamingResponse:
        return AsyncSinkCatalogWithStreamingResponse(self._catalog.sinks)

    @cached_property
    def sources(self) -> AsyncSourceCatalogWithStreamingResponse:
        return AsyncSourceCatalogWithStreamingResponse(self._catalog.sources)
