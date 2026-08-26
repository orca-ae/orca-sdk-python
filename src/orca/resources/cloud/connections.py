"""External connection definitions served by the `cloud.sn.io` extension.

Wire field names are mirrored verbatim throughout the cloud namespace; see
`orca.types.cloud_connection_shared` for why.
"""

from __future__ import annotations

from typing import Any, List, cast

import httpx2

from ._gate import cloud_gate, async_cloud_gate
from ...types import (
    cloud_connection_create_params,
    cloud_connection_update_params,
    cloud_connection_validate_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.cloud_connection import CloudConnection, CloudConnectionHealth
from ...types.cloud_connection_shared import CloudConnectionSpecParam, CloudConnectionStatusParam

__all__ = ["Connections", "AsyncConnections"]


class Connections(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConnectionsWithRawResponse:
        return ConnectionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConnectionsWithStreamingResponse:
        return ConnectionsWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> List[CloudConnection]:
        """
        List every stored external connection.

        The contract returns the whole set in one response; there is no cursor.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/connections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(Any, List[CloudConnection]),  # List types cannot be passed as arguments in the type system
        )

    def create(
        self,
        *,
        name: str | Omit = omit,
        spec: CloudConnectionSpecParam | Omit = omit,
        status: CloudConnectionStatusParam | Omit = omit,
        internal: bool | Omit = omit,
        clusterRef: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Create an external connection.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          name: Identifies the connection; it is the `{name}` every other method takes.

          spec: The connection itself. `spec.type` selects which of `kafka`, `pulsar`, or
              `other` carries the configuration.

          status: Server-owned. Accepted because the body is the whole document, but ignored.

          internal: Marks a connection the platform manages on your behalf.

          clusterRef: The cluster this connection belongs to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._post(
            "/apis/cloud.sn.io/v1/connections",
            body=maybe_transform(
                {
                    "name": name,
                    "spec": spec,
                    "status": status,
                    "internal": internal,
                    "clusterRef": clusterRef,
                },
                cloud_connection_create_params.CloudConnectionCreateParams,
            ),
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
    ) -> CloudConnection:
        """
        Retrieve one external connection.

        Args:
          name: The connection to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/connections/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudConnection,
        )

    def update(
        self,
        name: str,
        *,
        body_name: str | Omit = omit,
        spec: CloudConnectionSpecParam | Omit = omit,
        status: CloudConnectionStatusParam | Omit = omit,
        internal: bool | Omit = omit,
        clusterRef: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Replace an external connection.

        This is a `PUT`: the body replaces the stored document rather than merging
        into it, so send every field you want to keep. The contract declares no
        response schema, so the parsed body is returned as-is.

        Args:
          name: The connection to replace. This path segment is what the server acts on.

          body_name: The `name` field of the replacement document. The contract accepts it
              because the body is the whole connection, but the path decides which
              connection is replaced -- send it only to keep the stored document
              self-describing, and keep it equal to `name`.

          spec: The replacement connection configuration.

          status: Server-owned. Accepted because the body is the whole document, but ignored.

          internal: Marks a connection the platform manages on your behalf.

          clusterRef: The cluster this connection belongs to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._put(
            path_template("/apis/cloud.sn.io/v1/connections/{name}", name=name),
            body=maybe_transform(
                {
                    "name": body_name,
                    "spec": spec,
                    "status": status,
                    "internal": internal,
                    "clusterRef": clusterRef,
                },
                cloud_connection_update_params.CloudConnectionUpdateParams,
            ),
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
        Permanently delete an external connection.

        There is no archive for connections. The contract declares no response
        schema, so the parsed body is returned as-is.

        Args:
          name: The connection to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._delete(
            path_template("/apis/cloud.sn.io/v1/connections/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def test(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudConnectionHealth:
        """
        Test a stored external connection and report its health.

        The action is spelled as a colon suffix on the resource -- `{name}:test` --
        and it is a `GET`, not a `POST`: testing reports on the stored connection
        rather than changing it.

        Args:
          name: The connection to test.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/connections/{name}:test", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudConnectionHealth,
        )

    def validate(
        self,
        *,
        name: str | Omit = omit,
        spec: CloudConnectionSpecParam | Omit = omit,
        status: CloudConnectionStatusParam | Omit = omit,
        internal: bool | Omit = omit,
        clusterRef: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Validate a connection configuration without storing it.

        Unlike `test`, this takes the configuration in the body, so it answers
        "would this work?" for a connection that does not exist yet. The contract
        declares no response schema, so the parsed body is returned as-is.

        Args:
          name: Optional name to validate under; nothing is stored either way.

          spec: The connection configuration to check.

          status: Server-owned. Accepted because the body is the whole document, but ignored.

          internal: Marks a connection the platform manages on your behalf.

          clusterRef: The cluster this connection would belong to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._post(
            "/apis/cloud.sn.io/v1/connections/validate",
            body=maybe_transform(
                {
                    "name": name,
                    "spec": spec,
                    "status": status,
                    "internal": internal,
                    "clusterRef": clusterRef,
                },
                cloud_connection_validate_params.CloudConnectionValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncConnections(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConnectionsWithRawResponse:
        return AsyncConnectionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConnectionsWithStreamingResponse:
        return AsyncConnectionsWithStreamingResponse(self)

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> List[CloudConnection]:
        """
        List every stored external connection.

        The contract returns the whole set in one response; there is no cursor.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/connections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(Any, List[CloudConnection]),  # List types cannot be passed as arguments in the type system
        )

    async def create(
        self,
        *,
        name: str | Omit = omit,
        spec: CloudConnectionSpecParam | Omit = omit,
        status: CloudConnectionStatusParam | Omit = omit,
        internal: bool | Omit = omit,
        clusterRef: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Create an external connection.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          name: Identifies the connection; it is the `{name}` every other method takes.

          spec: The connection itself. `spec.type` selects which of `kafka`, `pulsar`, or
              `other` carries the configuration.

          status: Server-owned. Accepted because the body is the whole document, but ignored.

          internal: Marks a connection the platform manages on your behalf.

          clusterRef: The cluster this connection belongs to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._post(
            "/apis/cloud.sn.io/v1/connections",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "spec": spec,
                    "status": status,
                    "internal": internal,
                    "clusterRef": clusterRef,
                },
                cloud_connection_create_params.CloudConnectionCreateParams,
            ),
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
    ) -> CloudConnection:
        """
        Retrieve one external connection.

        Args:
          name: The connection to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/connections/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudConnection,
        )

    async def update(
        self,
        name: str,
        *,
        body_name: str | Omit = omit,
        spec: CloudConnectionSpecParam | Omit = omit,
        status: CloudConnectionStatusParam | Omit = omit,
        internal: bool | Omit = omit,
        clusterRef: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Replace an external connection.

        This is a `PUT`: the body replaces the stored document rather than merging
        into it, so send every field you want to keep. The contract declares no
        response schema, so the parsed body is returned as-is.

        Args:
          name: The connection to replace. This path segment is what the server acts on.

          body_name: The `name` field of the replacement document. The contract accepts it
              because the body is the whole connection, but the path decides which
              connection is replaced -- send it only to keep the stored document
              self-describing, and keep it equal to `name`.

          spec: The replacement connection configuration.

          status: Server-owned. Accepted because the body is the whole document, but ignored.

          internal: Marks a connection the platform manages on your behalf.

          clusterRef: The cluster this connection belongs to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._put(
            path_template("/apis/cloud.sn.io/v1/connections/{name}", name=name),
            body=await async_maybe_transform(
                {
                    "name": body_name,
                    "spec": spec,
                    "status": status,
                    "internal": internal,
                    "clusterRef": clusterRef,
                },
                cloud_connection_update_params.CloudConnectionUpdateParams,
            ),
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
        Permanently delete an external connection.

        There is no archive for connections. The contract declares no response
        schema, so the parsed body is returned as-is.

        Args:
          name: The connection to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._delete(
            path_template("/apis/cloud.sn.io/v1/connections/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def test(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudConnectionHealth:
        """
        Test a stored external connection and report its health.

        The action is spelled as a colon suffix on the resource -- `{name}:test` --
        and it is a `GET`, not a `POST`: testing reports on the stored connection
        rather than changing it.

        Args:
          name: The connection to test.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/connections/{name}:test", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudConnectionHealth,
        )

    async def validate(
        self,
        *,
        name: str | Omit = omit,
        spec: CloudConnectionSpecParam | Omit = omit,
        status: CloudConnectionStatusParam | Omit = omit,
        internal: bool | Omit = omit,
        clusterRef: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Validate a connection configuration without storing it.

        Unlike `test`, this takes the configuration in the body, so it answers
        "would this work?" for a connection that does not exist yet. The contract
        declares no response schema, so the parsed body is returned as-is.

        Args:
          name: Optional name to validate under; nothing is stored either way.

          spec: The connection configuration to check.

          status: Server-owned. Accepted because the body is the whole document, but ignored.

          internal: Marks a connection the platform manages on your behalf.

          clusterRef: The cluster this connection would belong to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._post(
            "/apis/cloud.sn.io/v1/connections/validate",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "spec": spec,
                    "status": status,
                    "internal": internal,
                    "clusterRef": clusterRef,
                },
                cloud_connection_validate_params.CloudConnectionValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ConnectionsWithRawResponse:
    def __init__(self, connections: Connections) -> None:
        self._connections = connections

        self.list = to_raw_response_wrapper(connections.list)
        self.create = to_raw_response_wrapper(connections.create)
        self.retrieve = to_raw_response_wrapper(connections.retrieve)
        self.update = to_raw_response_wrapper(connections.update)
        self.delete = to_raw_response_wrapper(connections.delete)
        self.test = to_raw_response_wrapper(connections.test)
        self.validate = to_raw_response_wrapper(connections.validate)


class AsyncConnectionsWithRawResponse:
    def __init__(self, connections: AsyncConnections) -> None:
        self._connections = connections

        self.list = async_to_raw_response_wrapper(connections.list)
        self.create = async_to_raw_response_wrapper(connections.create)
        self.retrieve = async_to_raw_response_wrapper(connections.retrieve)
        self.update = async_to_raw_response_wrapper(connections.update)
        self.delete = async_to_raw_response_wrapper(connections.delete)
        self.test = async_to_raw_response_wrapper(connections.test)
        self.validate = async_to_raw_response_wrapper(connections.validate)


class ConnectionsWithStreamingResponse:
    def __init__(self, connections: Connections) -> None:
        self._connections = connections

        self.list = to_streamed_response_wrapper(connections.list)
        self.create = to_streamed_response_wrapper(connections.create)
        self.retrieve = to_streamed_response_wrapper(connections.retrieve)
        self.update = to_streamed_response_wrapper(connections.update)
        self.delete = to_streamed_response_wrapper(connections.delete)
        self.test = to_streamed_response_wrapper(connections.test)
        self.validate = to_streamed_response_wrapper(connections.validate)


class AsyncConnectionsWithStreamingResponse:
    def __init__(self, connections: AsyncConnections) -> None:
        self._connections = connections

        self.list = async_to_streamed_response_wrapper(connections.list)
        self.create = async_to_streamed_response_wrapper(connections.create)
        self.retrieve = async_to_streamed_response_wrapper(connections.retrieve)
        self.update = async_to_streamed_response_wrapper(connections.update)
        self.delete = async_to_streamed_response_wrapper(connections.delete)
        self.test = async_to_streamed_response_wrapper(connections.test)
        self.validate = async_to_streamed_response_wrapper(connections.validate)
