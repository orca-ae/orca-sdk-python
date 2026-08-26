from __future__ import annotations

from typing import Any, cast

import httpx2

from ...types import (
    session_resource_add_params,
    session_resource_list_params,
    session_resource_update_params,
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
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.session_resource import (
    SessionResource,
    DeletedSessionResource,
    SessionResourceRequestParam,
)

__all__ = ["Resources", "AsyncResources"]


class Resources(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResourcesWithRawResponse:
        return ResourcesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResourcesWithStreamingResponse:
        return ResourcesWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[SessionResource]:
        """
        List the resources attached to a session.

        Args:
          session_id: The session whose resources to list.

          limit: Maximum number of resources to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/resources", session_id=session_id),
            page=SyncPageCursor[SessionResource],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    session_resource_list_params.SessionResourceListParams,
                ),
            ),
            model=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
        )

    def add(
        self,
        session_id: str,
        *,
        resource: SessionResourceRequestParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionResource:
        """
        Attach a resource to a session.

        Args:
          session_id: The session to attach to.

          resource: The resource to attach, discriminated on `type`. This is the whole request
              body, which is why it is one argument rather than a set of flattened fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return cast(
            SessionResource,
            self._post(
                path_template("/v1/sessions/{session_id}/resources", session_id=session_id),
                body=maybe_transform(resource, session_resource_add_params.SessionResourceAddParams),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        session_id: str,
        resource_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionResource:
        """
        Retrieve one resource attached to a session.

        Args:
          session_id: The session that owns the resource.

          resource_id: The resource to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not resource_id:
            raise ValueError(f"Expected a non-empty value for `resource_id` but received {resource_id!r}")
        return cast(
            SessionResource,
            self._get(
                path_template(
                    "/v1/sessions/{session_id}/resources/{resource_id}",
                    session_id=session_id,
                    resource_id=resource_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def update(
        self,
        session_id: str,
        resource_id: str,
        *,
        authorization_token: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionResource:
        """
        Rotate a repository resource's authorization token.

        Uses POST, matching the contract. The token is write-only: it is never
        returned on the resource, so rotating it is the only way to change it.

        Args:
          session_id: The session that owns the resource.

          resource_id: The resource to update.

          authorization_token: Replacement token.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not resource_id:
            raise ValueError(f"Expected a non-empty value for `resource_id` but received {resource_id!r}")
        return cast(
            SessionResource,
            self._post(
                path_template(
                    "/v1/sessions/{session_id}/resources/{resource_id}",
                    session_id=session_id,
                    resource_id=resource_id,
                ),
                body=maybe_transform(
                    {"authorization_token": authorization_token},
                    session_resource_update_params.SessionResourceUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def delete(
        self,
        session_id: str,
        resource_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSessionResource:
        """
        Detach a resource from a session and return its tombstone.

        Args:
          session_id: The session that owns the resource.

          resource_id: The resource to remove.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not resource_id:
            raise ValueError(f"Expected a non-empty value for `resource_id` but received {resource_id!r}")
        return self._delete(
            path_template(
                "/v1/sessions/{session_id}/resources/{resource_id}",
                session_id=session_id,
                resource_id=resource_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSessionResource,
        )


class AsyncResources(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResourcesWithRawResponse:
        return AsyncResourcesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResourcesWithStreamingResponse:
        return AsyncResourcesWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SessionResource, AsyncPageCursor[SessionResource]]:
        """
        List the resources attached to a session.

        Args:
          session_id: The session whose resources to list.

          limit: Maximum number of resources to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/resources", session_id=session_id),
            page=AsyncPageCursor[SessionResource],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    session_resource_list_params.SessionResourceListParams,
                ),
            ),
            model=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
        )

    async def add(
        self,
        session_id: str,
        *,
        resource: SessionResourceRequestParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionResource:
        """
        Attach a resource to a session.

        Args:
          session_id: The session to attach to.

          resource: The resource to attach, discriminated on `type`. This is the whole request
              body, which is why it is one argument rather than a set of flattened fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return cast(
            SessionResource,
            await self._post(
                path_template("/v1/sessions/{session_id}/resources", session_id=session_id),
                body=await async_maybe_transform(resource, session_resource_add_params.SessionResourceAddParams),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        session_id: str,
        resource_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionResource:
        """
        Retrieve one resource attached to a session.

        Args:
          session_id: The session that owns the resource.

          resource_id: The resource to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not resource_id:
            raise ValueError(f"Expected a non-empty value for `resource_id` but received {resource_id!r}")
        return cast(
            SessionResource,
            await self._get(
                path_template(
                    "/v1/sessions/{session_id}/resources/{resource_id}",
                    session_id=session_id,
                    resource_id=resource_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def update(
        self,
        session_id: str,
        resource_id: str,
        *,
        authorization_token: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionResource:
        """
        Rotate a repository resource's authorization token.

        Uses POST, matching the contract. The token is write-only: it is never
        returned on the resource, so rotating it is the only way to change it.

        Args:
          session_id: The session that owns the resource.

          resource_id: The resource to update.

          authorization_token: Replacement token.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not resource_id:
            raise ValueError(f"Expected a non-empty value for `resource_id` but received {resource_id!r}")
        return cast(
            SessionResource,
            await self._post(
                path_template(
                    "/v1/sessions/{session_id}/resources/{resource_id}",
                    session_id=session_id,
                    resource_id=resource_id,
                ),
                body=await async_maybe_transform(
                    {"authorization_token": authorization_token},
                    session_resource_update_params.SessionResourceUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionResource),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def delete(
        self,
        session_id: str,
        resource_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSessionResource:
        """
        Detach a resource from a session and return its tombstone.

        Args:
          session_id: The session that owns the resource.

          resource_id: The resource to remove.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not resource_id:
            raise ValueError(f"Expected a non-empty value for `resource_id` but received {resource_id!r}")
        return await self._delete(
            path_template(
                "/v1/sessions/{session_id}/resources/{resource_id}",
                session_id=session_id,
                resource_id=resource_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSessionResource,
        )


class ResourcesWithRawResponse:
    def __init__(self, resources: Resources) -> None:
        self._resources = resources

        self.list = to_raw_response_wrapper(resources.list)
        self.add = to_raw_response_wrapper(resources.add)
        self.retrieve = to_raw_response_wrapper(resources.retrieve)
        self.update = to_raw_response_wrapper(resources.update)
        self.delete = to_raw_response_wrapper(resources.delete)


class AsyncResourcesWithRawResponse:
    def __init__(self, resources: AsyncResources) -> None:
        self._resources = resources

        self.list = async_to_raw_response_wrapper(resources.list)
        self.add = async_to_raw_response_wrapper(resources.add)
        self.retrieve = async_to_raw_response_wrapper(resources.retrieve)
        self.update = async_to_raw_response_wrapper(resources.update)
        self.delete = async_to_raw_response_wrapper(resources.delete)


class ResourcesWithStreamingResponse:
    def __init__(self, resources: Resources) -> None:
        self._resources = resources

        self.list = to_streamed_response_wrapper(resources.list)
        self.add = to_streamed_response_wrapper(resources.add)
        self.retrieve = to_streamed_response_wrapper(resources.retrieve)
        self.update = to_streamed_response_wrapper(resources.update)
        self.delete = to_streamed_response_wrapper(resources.delete)


class AsyncResourcesWithStreamingResponse:
    def __init__(self, resources: AsyncResources) -> None:
        self._resources = resources

        self.list = async_to_streamed_response_wrapper(resources.list)
        self.add = async_to_streamed_response_wrapper(resources.add)
        self.retrieve = async_to_streamed_response_wrapper(resources.retrieve)
        self.update = async_to_streamed_response_wrapper(resources.update)
        self.delete = async_to_streamed_response_wrapper(resources.delete)
