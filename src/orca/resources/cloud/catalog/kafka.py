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
from ....types.cloud_catalog import CloudCatalogConnectorList, CloudCatalogConfigFieldList

__all__ = ["KafkaCatalog", "AsyncKafkaCatalog"]


class KafkaCatalog(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> KafkaCatalogWithRawResponse:
        return KafkaCatalogWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KafkaCatalogWithStreamingResponse:
        return KafkaCatalogWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudCatalogConnectorList:
        """
        List the Kafka connector definitions this deployment offers.

        The catalog is read-only and served whole -- it is not paginated. A definition
        names the connector; call `retrieve()` for the fields it accepts.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/catalog/kafka",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudCatalogConnectorList,
        )

    def retrieve(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudCatalogConfigFieldList:
        """
        Retrieve the configuration fields a Kafka connector accepts.

        The response is the field list, not the connector definition: `list()` says
        which connectors exist, this says how to configure one of them.

        Args:
          name: Catalog name of the connector, as reported by `list()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/catalog/kafka/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudCatalogConfigFieldList,
        )


class AsyncKafkaCatalog(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncKafkaCatalogWithRawResponse:
        return AsyncKafkaCatalogWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKafkaCatalogWithStreamingResponse:
        return AsyncKafkaCatalogWithStreamingResponse(self)

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudCatalogConnectorList:
        """
        List the Kafka connector definitions this deployment offers.

        The catalog is read-only and served whole -- it is not paginated. A definition
        names the connector; call `retrieve()` for the fields it accepts.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/catalog/kafka",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudCatalogConnectorList,
        )

    async def retrieve(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudCatalogConfigFieldList:
        """
        Retrieve the configuration fields a Kafka connector accepts.

        The response is the field list, not the connector definition: `list()` says
        which connectors exist, this says how to configure one of them.

        Args:
          name: Catalog name of the connector, as reported by `list()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/catalog/kafka/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudCatalogConfigFieldList,
        )


class KafkaCatalogWithRawResponse:
    def __init__(self, kafka_catalog: KafkaCatalog) -> None:
        self._kafka_catalog = kafka_catalog

        self.list = to_raw_response_wrapper(kafka_catalog.list)
        self.retrieve = to_raw_response_wrapper(kafka_catalog.retrieve)


class AsyncKafkaCatalogWithRawResponse:
    def __init__(self, kafka_catalog: AsyncKafkaCatalog) -> None:
        self._kafka_catalog = kafka_catalog

        self.list = async_to_raw_response_wrapper(kafka_catalog.list)
        self.retrieve = async_to_raw_response_wrapper(kafka_catalog.retrieve)


class KafkaCatalogWithStreamingResponse:
    def __init__(self, kafka_catalog: KafkaCatalog) -> None:
        self._kafka_catalog = kafka_catalog

        self.list = to_streamed_response_wrapper(kafka_catalog.list)
        self.retrieve = to_streamed_response_wrapper(kafka_catalog.retrieve)


class AsyncKafkaCatalogWithStreamingResponse:
    def __init__(self, kafka_catalog: AsyncKafkaCatalog) -> None:
        self._kafka_catalog = kafka_catalog

        self.list = async_to_streamed_response_wrapper(kafka_catalog.list)
        self.retrieve = async_to_streamed_response_wrapper(kafka_catalog.retrieve)
