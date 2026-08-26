from __future__ import annotations

import httpx2

from ...types import memory_version_list_params, memory_version_retrieve_params
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
from ...types.memory import MemoryView
from ...types.memory_version import MemoryVersion, MemoryVersionOperation

__all__ = ["MemoryVersions", "AsyncMemoryVersions"]


class MemoryVersions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MemoryVersionsWithRawResponse:
        return MemoryVersionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemoryVersionsWithStreamingResponse:
        return MemoryVersionsWithStreamingResponse(self)

    def list(
        self,
        memory_store_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        memory_id: str | Omit = omit,
        api_key_id: str | Omit = omit,
        operation: MemoryVersionOperation | Omit = omit,
        created_at_gte: str | Omit = omit,
        created_at_lte: str | Omit = omit,
        view: MemoryView | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[MemoryVersion]:
        """
        List the audit trail of memory versions in a memory store.

        Args:
          memory_store_id: The memory store whose versions to list.

          limit: Maximum number of versions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          memory_id: Only versions of this memory.

          api_key_id: Only versions written by this API key.

          operation: Only versions recording this operation.

          created_at_gte: Sent as `created_at[gte]`.

          created_at_lte: Sent as `created_at[lte]`.

          view: `full` includes each version's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._get_api_list(
            path_template("/v1/memory_stores/{memory_store_id}/memory_versions", memory_store_id=memory_store_id),
            page=SyncPageCursor[MemoryVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "memory_id": memory_id,
                        "api_key_id": api_key_id,
                        "operation": operation,
                        "created_at_gte": created_at_gte,
                        "created_at_lte": created_at_lte,
                        "view": view,
                    },
                    memory_version_list_params.MemoryVersionListParams,
                ),
            ),
            model=MemoryVersion,
        )

    def retrieve(
        self,
        memory_store_id: str,
        memory_version_id: str,
        *,
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryVersion:
        """
        Retrieve a memory version.

        Args:
          memory_store_id: The memory store holding the version.

          memory_version_id: The version to retrieve.

          view: `full` returns the version's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_version_id:
            raise ValueError(f"Expected a non-empty value for `memory_version_id` but received {memory_version_id!r}")
        return self._get(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}",
                memory_store_id=memory_store_id,
                memory_version_id=memory_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, memory_version_retrieve_params.MemoryVersionRetrieveParams),
            ),
            cast_to=MemoryVersion,
        )

    def redact(
        self,
        memory_store_id: str,
        memory_version_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryVersion:
        """
        Redact a memory version and return the redacted snapshot.

        Redaction drops the version's stored content while keeping the audit entry
        itself, so the trail stays complete. It cannot be undone.

        Args:
          memory_store_id: The memory store holding the version.

          memory_version_id: The version to redact.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_version_id:
            raise ValueError(f"Expected a non-empty value for `memory_version_id` but received {memory_version_id!r}")
        return self._post(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact",
                memory_store_id=memory_store_id,
                memory_version_id=memory_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryVersion,
        )


class AsyncMemoryVersions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMemoryVersionsWithRawResponse:
        return AsyncMemoryVersionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemoryVersionsWithStreamingResponse:
        return AsyncMemoryVersionsWithStreamingResponse(self)

    def list(
        self,
        memory_store_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        memory_id: str | Omit = omit,
        api_key_id: str | Omit = omit,
        operation: MemoryVersionOperation | Omit = omit,
        created_at_gte: str | Omit = omit,
        created_at_lte: str | Omit = omit,
        view: MemoryView | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MemoryVersion, AsyncPageCursor[MemoryVersion]]:
        """
        List the audit trail of memory versions in a memory store.

        Args:
          memory_store_id: The memory store whose versions to list.

          limit: Maximum number of versions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          memory_id: Only versions of this memory.

          api_key_id: Only versions written by this API key.

          operation: Only versions recording this operation.

          created_at_gte: Sent as `created_at[gte]`.

          created_at_lte: Sent as `created_at[lte]`.

          view: `full` includes each version's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._get_api_list(
            path_template("/v1/memory_stores/{memory_store_id}/memory_versions", memory_store_id=memory_store_id),
            page=AsyncPageCursor[MemoryVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "memory_id": memory_id,
                        "api_key_id": api_key_id,
                        "operation": operation,
                        "created_at_gte": created_at_gte,
                        "created_at_lte": created_at_lte,
                        "view": view,
                    },
                    memory_version_list_params.MemoryVersionListParams,
                ),
            ),
            model=MemoryVersion,
        )

    async def retrieve(
        self,
        memory_store_id: str,
        memory_version_id: str,
        *,
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryVersion:
        """
        Retrieve a memory version.

        Args:
          memory_store_id: The memory store holding the version.

          memory_version_id: The version to retrieve.

          view: `full` returns the version's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_version_id:
            raise ValueError(f"Expected a non-empty value for `memory_version_id` but received {memory_version_id!r}")
        return await self._get(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}",
                memory_store_id=memory_store_id,
                memory_version_id=memory_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"view": view}, memory_version_retrieve_params.MemoryVersionRetrieveParams
                ),
            ),
            cast_to=MemoryVersion,
        )

    async def redact(
        self,
        memory_store_id: str,
        memory_version_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryVersion:
        """
        Redact a memory version and return the redacted snapshot.

        Redaction drops the version's stored content while keeping the audit entry
        itself, so the trail stays complete. It cannot be undone.

        Args:
          memory_store_id: The memory store holding the version.

          memory_version_id: The version to redact.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_version_id:
            raise ValueError(f"Expected a non-empty value for `memory_version_id` but received {memory_version_id!r}")
        return await self._post(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact",
                memory_store_id=memory_store_id,
                memory_version_id=memory_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryVersion,
        )


class MemoryVersionsWithRawResponse:
    def __init__(self, memory_versions: MemoryVersions) -> None:
        self._memory_versions = memory_versions

        self.list = to_raw_response_wrapper(memory_versions.list)
        self.retrieve = to_raw_response_wrapper(memory_versions.retrieve)
        self.redact = to_raw_response_wrapper(memory_versions.redact)


class AsyncMemoryVersionsWithRawResponse:
    def __init__(self, memory_versions: AsyncMemoryVersions) -> None:
        self._memory_versions = memory_versions

        self.list = async_to_raw_response_wrapper(memory_versions.list)
        self.retrieve = async_to_raw_response_wrapper(memory_versions.retrieve)
        self.redact = async_to_raw_response_wrapper(memory_versions.redact)


class MemoryVersionsWithStreamingResponse:
    def __init__(self, memory_versions: MemoryVersions) -> None:
        self._memory_versions = memory_versions

        self.list = to_streamed_response_wrapper(memory_versions.list)
        self.retrieve = to_streamed_response_wrapper(memory_versions.retrieve)
        self.redact = to_streamed_response_wrapper(memory_versions.redact)


class AsyncMemoryVersionsWithStreamingResponse:
    def __init__(self, memory_versions: AsyncMemoryVersions) -> None:
        self._memory_versions = memory_versions

        self.list = async_to_streamed_response_wrapper(memory_versions.list)
        self.retrieve = async_to_streamed_response_wrapper(memory_versions.retrieve)
        self.redact = async_to_streamed_response_wrapper(memory_versions.redact)
