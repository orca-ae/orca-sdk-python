from __future__ import annotations

import httpx2

from ..._gate import cloud_gate, async_cloud_gate
from .....types import cloud_kafka_plugin_list_params
from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import path_template, maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.cloud_kafka_plugin import (
    CloudKafkaPluginInfoList,
    CloudKafkaConfigKeyInfoList,
    CloudKafkaPluginCatalogEntryList,
)

__all__ = ["Plugins", "AsyncPlugins"]

_PLUGINS = "/apis/cloud.sn.io/v1/connectors/kafka/connector-plugins"


class Plugins(SyncAPIResource):
    """Connector plugin discovery.

    Configuration *validation* is deliberately absent. The contract declares
    `PUT .../connector-plugins/{pluginName}/config/validate` with a single HTTP 400
    response saying validation is unsupported, so there is no successful call to
    expose and the SDK does not offer one.
    """

    @cached_property
    def with_raw_response(self) -> PluginsWithRawResponse:
        return PluginsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PluginsWithStreamingResponse:
        return PluginsWithStreamingResponse(self)

    def list(
        self,
        *,
        connectors_only: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaPluginInfoList:
        """
        List the plugins installed on the worker.

        Args:
          connectors_only: List only connector plugins instead of every plugin the worker has loaded.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            _PLUGINS,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"connectorsOnly": connectors_only},
                    cloud_kafka_plugin_list_params.CloudKafkaPluginListParams,
                ),
            ),
            cast_to=CloudKafkaPluginInfoList,
        )

    def retrieve_config(
        self,
        plugin_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConfigKeyInfoList:
        """
        Retrieve the configuration keys a plugin accepts.

        Args:
          plugin_name: Plugin class name, as reported by `list()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not plugin_name:
            raise ValueError(f"Expected a non-empty value for `plugin_name` but received {plugin_name!r}")
        return self._get(
            path_template(_PLUGINS + "/{plugin_name}/config", plugin_name=plugin_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConfigKeyInfoList,
        )

    def list_catalog(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaPluginCatalogEntryList:
        """
        List the plugin catalog.

        The catalog describes what is *installable* -- packaging, icons, per-field
        metadata -- whereas `list()` reports what the worker has already loaded.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            _PLUGINS + "/catalog",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaPluginCatalogEntryList,
        )


class AsyncPlugins(AsyncAPIResource):
    """Connector plugin discovery.

    Configuration *validation* is deliberately absent. The contract declares
    `PUT .../connector-plugins/{pluginName}/config/validate` with a single HTTP 400
    response saying validation is unsupported, so there is no successful call to
    expose and the SDK does not offer one.
    """

    @cached_property
    def with_raw_response(self) -> AsyncPluginsWithRawResponse:
        return AsyncPluginsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPluginsWithStreamingResponse:
        return AsyncPluginsWithStreamingResponse(self)

    async def list(
        self,
        *,
        connectors_only: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaPluginInfoList:
        """
        List the plugins installed on the worker.

        Args:
          connectors_only: List only connector plugins instead of every plugin the worker has loaded.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            _PLUGINS,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"connectorsOnly": connectors_only},
                    cloud_kafka_plugin_list_params.CloudKafkaPluginListParams,
                ),
            ),
            cast_to=CloudKafkaPluginInfoList,
        )

    async def retrieve_config(
        self,
        plugin_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConfigKeyInfoList:
        """
        Retrieve the configuration keys a plugin accepts.

        Args:
          plugin_name: Plugin class name, as reported by `list()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not plugin_name:
            raise ValueError(f"Expected a non-empty value for `plugin_name` but received {plugin_name!r}")
        return await self._get(
            path_template(_PLUGINS + "/{plugin_name}/config", plugin_name=plugin_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConfigKeyInfoList,
        )

    async def list_catalog(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaPluginCatalogEntryList:
        """
        List the plugin catalog.

        The catalog describes what is *installable* -- packaging, icons, per-field
        metadata -- whereas `list()` reports what the worker has already loaded.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            _PLUGINS + "/catalog",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaPluginCatalogEntryList,
        )


class PluginsWithRawResponse:
    def __init__(self, plugins: Plugins) -> None:
        self._plugins = plugins

        self.list = to_raw_response_wrapper(plugins.list)
        self.retrieve_config = to_raw_response_wrapper(plugins.retrieve_config)
        self.list_catalog = to_raw_response_wrapper(plugins.list_catalog)


class AsyncPluginsWithRawResponse:
    def __init__(self, plugins: AsyncPlugins) -> None:
        self._plugins = plugins

        self.list = async_to_raw_response_wrapper(plugins.list)
        self.retrieve_config = async_to_raw_response_wrapper(plugins.retrieve_config)
        self.list_catalog = async_to_raw_response_wrapper(plugins.list_catalog)


class PluginsWithStreamingResponse:
    def __init__(self, plugins: Plugins) -> None:
        self._plugins = plugins

        self.list = to_streamed_response_wrapper(plugins.list)
        self.retrieve_config = to_streamed_response_wrapper(plugins.retrieve_config)
        self.list_catalog = to_streamed_response_wrapper(plugins.list_catalog)


class AsyncPluginsWithStreamingResponse:
    def __init__(self, plugins: AsyncPlugins) -> None:
        self._plugins = plugins

        self.list = async_to_streamed_response_wrapper(plugins.list)
        self.retrieve_config = async_to_streamed_response_wrapper(plugins.retrieve_config)
        self.list_catalog = async_to_streamed_response_wrapper(plugins.list_catalog)
