from __future__ import annotations

from typing import Mapping, cast

import httpx2

from .._gate import cloud_gate, async_cloud_gate
from ....types import cloud_connector_sink_create_params, cloud_connector_sink_update_params
from ...._files import deepcopy_with_paths
from ...._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from ...._utils import transform, extract_files, path_template, async_transform
from ...._compat import cached_property
from .._multipart import encode_cloud_multipart
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.cloud_connector_sink import (
    CloudSinkConfig,
    CloudSinkStatus,
    CloudSinkNameList,
    CloudSinkConfigParam,
    CloudSinkInstanceStatus,
)
from ....types.cloud_connector_shared import CloudRuntimeUpdateOptionsParam

__all__ = ["SinkConnectors", "AsyncSinkConnectors"]


class SinkConnectors(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SinkConnectorsWithRawResponse:
        return SinkConnectorsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SinkConnectorsWithStreamingResponse:
        return SinkConnectorsWithStreamingResponse(self)

    def create(
        self,
        name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        sink_config: CloudSinkConfigParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Register a sink connector.

        The body is `multipart/form-data`: the connector package arrives either inline
        as `data` or as a `url` the server fetches, and `sink_config` travels as its own
        JSON part rather than as flattened form fields. The success response carries no
        modelled body.

        Args:
          name: Name to register the sink under.

          data: The connector package bytes, when uploading rather than referencing a URL.

          url: Location the server fetches the connector package from.

          sink_config: The sink's configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        body = deepcopy_with_paths(
            {"data": data, "url": url, "sinkConfig": sink_config},
            paths=[["data"]],
        )
        uploads = extract_files(cast(Mapping[str, object], body), paths=[["data"]])
        fields, json_parts = encode_cloud_multipart(
            transform(body, cloud_connector_sink_create_params.CloudSinkCreateParams)
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            body=fields,
            files=[*uploads, *json_parts],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkConfig:
        """
        Retrieve a sink connector's configuration.

        Args:
          name: The sink to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkConfig,
        )

    def update(
        self,
        name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        sink_config: CloudSinkConfigParam | Omit = omit,
        update_options: CloudRuntimeUpdateOptionsParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Replace a sink connector's configuration.

        `PUT`, not a partial update: send the whole `sink_config`, because fields you
        leave out are dropped rather than preserved. The success response carries no
        modelled body.

        Args:
          name: The sink to update.

          data: The connector package bytes, when uploading rather than referencing a URL.

          url: Location the server fetches the connector package from.

          sink_config: The sink's complete replacement configuration.

          update_options: Options that change how the update is applied, such as whether stored
              authentication data is replaced.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        body = deepcopy_with_paths(
            {
                "data": data,
                "url": url,
                "sinkConfig": sink_config,
                "updateOptions": update_options,
            },
            paths=[["data"]],
        )
        uploads = extract_files(cast(Mapping[str, object], body), paths=[["data"]])
        fields, json_parts = encode_cloud_multipart(
            transform(body, cloud_connector_sink_update_params.CloudSinkUpdateParams)
        )
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._put(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            body=fields,
            files=[*uploads, *json_parts],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def delete(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Deregister a sink connector.

        This removes the connector outright; there is no archived state to come back
        to. The success response carries no modelled body.

        Args:
          name: The sink to deregister.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve_instance_status(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkInstanceStatus:
        """
        Retrieve the runtime counters for one sink connector instance.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance, as reported by `retrieve_status()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        return self._get(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}/status", name=name, instance_id=instance_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkInstanceStatus,
        )

    def retrieve_status(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkStatus:
        """
        Retrieve aggregate status across every instance of a sink connector.

        Args:
          name: The sink to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}/status", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkStatus,
        )

    def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkNameList:
        """
        List the names of every registered sink connector.

        The listing is names only and is served whole -- no cloud endpoint paginates.
        Call `retrieve()` for one connector's configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/connectors/sinks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkNameList,
        )

    def restart(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart every instance of a sink connector.

        The action lives in the path as a `:restart` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink to restart.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name) + ":restart",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def restart_instance(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart one instance of a sink connector.

        The action lives in the path as a `:restart` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance to restart.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}", name=name, instance_id=instance_id
            )
            + ":restart",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def start(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start every instance of a sink connector.

        The action lives in the path as a `:start` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink to start.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name) + ":start",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def start_instance(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start one instance of a sink connector.

        The action lives in the path as a `:start` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance to start.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}", name=name, instance_id=instance_id
            )
            + ":start",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def stop(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop every instance of a sink connector.

        The action lives in the path as a `:stop` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name) + ":stop",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def stop_instance(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop one instance of a sink connector.

        The action lives in the path as a `:stop` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}", name=name, instance_id=instance_id
            )
            + ":stop",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncSinkConnectors(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSinkConnectorsWithRawResponse:
        return AsyncSinkConnectorsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSinkConnectorsWithStreamingResponse:
        return AsyncSinkConnectorsWithStreamingResponse(self)

    async def create(
        self,
        name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        sink_config: CloudSinkConfigParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Register a sink connector.

        The body is `multipart/form-data`: the connector package arrives either inline
        as `data` or as a `url` the server fetches, and `sink_config` travels as its own
        JSON part rather than as flattened form fields. The success response carries no
        modelled body.

        Args:
          name: Name to register the sink under.

          data: The connector package bytes, when uploading rather than referencing a URL.

          url: Location the server fetches the connector package from.

          sink_config: The sink's configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        body = deepcopy_with_paths(
            {"data": data, "url": url, "sinkConfig": sink_config},
            paths=[["data"]],
        )
        uploads = extract_files(cast(Mapping[str, object], body), paths=[["data"]])
        fields, json_parts = encode_cloud_multipart(
            await async_transform(body, cloud_connector_sink_create_params.CloudSinkCreateParams)
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            body=fields,
            files=[*uploads, *json_parts],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkConfig:
        """
        Retrieve a sink connector's configuration.

        Args:
          name: The sink to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkConfig,
        )

    async def update(
        self,
        name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        sink_config: CloudSinkConfigParam | Omit = omit,
        update_options: CloudRuntimeUpdateOptionsParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Replace a sink connector's configuration.

        `PUT`, not a partial update: send the whole `sink_config`, because fields you
        leave out are dropped rather than preserved. The success response carries no
        modelled body.

        Args:
          name: The sink to update.

          data: The connector package bytes, when uploading rather than referencing a URL.

          url: Location the server fetches the connector package from.

          sink_config: The sink's complete replacement configuration.

          update_options: Options that change how the update is applied, such as whether stored
              authentication data is replaced.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        body = deepcopy_with_paths(
            {
                "data": data,
                "url": url,
                "sinkConfig": sink_config,
                "updateOptions": update_options,
            },
            paths=[["data"]],
        )
        uploads = extract_files(cast(Mapping[str, object], body), paths=[["data"]])
        fields, json_parts = encode_cloud_multipart(
            await async_transform(body, cloud_connector_sink_update_params.CloudSinkUpdateParams)
        )
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._put(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            body=fields,
            files=[*uploads, *json_parts],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def delete(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Deregister a sink connector.

        This removes the connector outright; there is no archived state to come back
        to. The success response carries no modelled body.

        Args:
          name: The sink to deregister.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve_instance_status(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkInstanceStatus:
        """
        Retrieve the runtime counters for one sink connector instance.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance, as reported by `retrieve_status()`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        return await self._get(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}/status", name=name, instance_id=instance_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkInstanceStatus,
        )

    async def retrieve_status(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkStatus:
        """
        Retrieve aggregate status across every instance of a sink connector.

        Args:
          name: The sink to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}/status", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkStatus,
        )

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudSinkNameList:
        """
        List the names of every registered sink connector.

        The listing is names only and is served whole -- no cloud endpoint paginates.
        Call `retrieve()` for one connector's configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/connectors/sinks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSinkNameList,
        )

    async def restart(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart every instance of a sink connector.

        The action lives in the path as a `:restart` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink to restart.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name) + ":restart",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def restart_instance(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart one instance of a sink connector.

        The action lives in the path as a `:restart` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance to restart.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}", name=name, instance_id=instance_id
            )
            + ":restart",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def start(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start every instance of a sink connector.

        The action lives in the path as a `:start` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink to start.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name) + ":start",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def start_instance(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start one instance of a sink connector.

        The action lives in the path as a `:start` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance to start.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}", name=name, instance_id=instance_id
            )
            + ":start",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def stop(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop every instance of a sink connector.

        The action lives in the path as a `:stop` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/connectors/sinks/{name}", name=name) + ":stop",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def stop_instance(
        self,
        name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop one instance of a sink connector.

        The action lives in the path as a `:stop` suffix, which the contract spells
        literally. The success response carries no modelled body.

        Args:
          name: The sink the instance belongs to.

          instance_id: Zero-based index of the instance to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/connectors/sinks/{name}/{instance_id}", name=name, instance_id=instance_id
            )
            + ":stop",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class SinkConnectorsWithRawResponse:
    def __init__(self, sinks: SinkConnectors) -> None:
        self._sinks = sinks

        self.create = to_raw_response_wrapper(sinks.create)
        self.retrieve = to_raw_response_wrapper(sinks.retrieve)
        self.update = to_raw_response_wrapper(sinks.update)
        self.delete = to_raw_response_wrapper(sinks.delete)
        self.retrieve_instance_status = to_raw_response_wrapper(sinks.retrieve_instance_status)
        self.retrieve_status = to_raw_response_wrapper(sinks.retrieve_status)
        self.list = to_raw_response_wrapper(sinks.list)
        self.restart = to_raw_response_wrapper(sinks.restart)
        self.restart_instance = to_raw_response_wrapper(sinks.restart_instance)
        self.start = to_raw_response_wrapper(sinks.start)
        self.start_instance = to_raw_response_wrapper(sinks.start_instance)
        self.stop = to_raw_response_wrapper(sinks.stop)
        self.stop_instance = to_raw_response_wrapper(sinks.stop_instance)


class AsyncSinkConnectorsWithRawResponse:
    def __init__(self, sinks: AsyncSinkConnectors) -> None:
        self._sinks = sinks

        self.create = async_to_raw_response_wrapper(sinks.create)
        self.retrieve = async_to_raw_response_wrapper(sinks.retrieve)
        self.update = async_to_raw_response_wrapper(sinks.update)
        self.delete = async_to_raw_response_wrapper(sinks.delete)
        self.retrieve_instance_status = async_to_raw_response_wrapper(sinks.retrieve_instance_status)
        self.retrieve_status = async_to_raw_response_wrapper(sinks.retrieve_status)
        self.list = async_to_raw_response_wrapper(sinks.list)
        self.restart = async_to_raw_response_wrapper(sinks.restart)
        self.restart_instance = async_to_raw_response_wrapper(sinks.restart_instance)
        self.start = async_to_raw_response_wrapper(sinks.start)
        self.start_instance = async_to_raw_response_wrapper(sinks.start_instance)
        self.stop = async_to_raw_response_wrapper(sinks.stop)
        self.stop_instance = async_to_raw_response_wrapper(sinks.stop_instance)


class SinkConnectorsWithStreamingResponse:
    def __init__(self, sinks: SinkConnectors) -> None:
        self._sinks = sinks

        self.create = to_streamed_response_wrapper(sinks.create)
        self.retrieve = to_streamed_response_wrapper(sinks.retrieve)
        self.update = to_streamed_response_wrapper(sinks.update)
        self.delete = to_streamed_response_wrapper(sinks.delete)
        self.retrieve_instance_status = to_streamed_response_wrapper(sinks.retrieve_instance_status)
        self.retrieve_status = to_streamed_response_wrapper(sinks.retrieve_status)
        self.list = to_streamed_response_wrapper(sinks.list)
        self.restart = to_streamed_response_wrapper(sinks.restart)
        self.restart_instance = to_streamed_response_wrapper(sinks.restart_instance)
        self.start = to_streamed_response_wrapper(sinks.start)
        self.start_instance = to_streamed_response_wrapper(sinks.start_instance)
        self.stop = to_streamed_response_wrapper(sinks.stop)
        self.stop_instance = to_streamed_response_wrapper(sinks.stop_instance)


class AsyncSinkConnectorsWithStreamingResponse:
    def __init__(self, sinks: AsyncSinkConnectors) -> None:
        self._sinks = sinks

        self.create = async_to_streamed_response_wrapper(sinks.create)
        self.retrieve = async_to_streamed_response_wrapper(sinks.retrieve)
        self.update = async_to_streamed_response_wrapper(sinks.update)
        self.delete = async_to_streamed_response_wrapper(sinks.delete)
        self.retrieve_instance_status = async_to_streamed_response_wrapper(sinks.retrieve_instance_status)
        self.retrieve_status = async_to_streamed_response_wrapper(sinks.retrieve_status)
        self.list = async_to_streamed_response_wrapper(sinks.list)
        self.restart = async_to_streamed_response_wrapper(sinks.restart)
        self.restart_instance = async_to_streamed_response_wrapper(sinks.restart_instance)
        self.start = async_to_streamed_response_wrapper(sinks.start)
        self.start_instance = async_to_streamed_response_wrapper(sinks.start_instance)
        self.stop = async_to_streamed_response_wrapper(sinks.stop)
        self.stop_instance = async_to_streamed_response_wrapper(sinks.stop_instance)
