from __future__ import annotations

from typing import Any, Optional, cast
from typing_extensions import Literal

import httpx2

from ...types import (
    memory_list_params,
    memory_create_params,
    memory_delete_params,
    memory_update_params,
    memory_retrieve_params,
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
from ...types.memory import Memory, MemoryView, DeletedMemory, MemoryListItem
from ...types.memory_update_params import MemoryContentSha256PreconditionParam

__all__ = ["Memories", "AsyncMemories"]


class Memories(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MemoriesWithRawResponse:
        return MemoriesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemoriesWithStreamingResponse:
        return MemoriesWithStreamingResponse(self)

    def list(
        self,
        memory_store_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        depth: Optional[Literal[0, 1]] | Omit = omit,
        path_prefix: str | Omit = omit,
        view: MemoryView | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[MemoryListItem]:
        """
        List memories in a memory store.

        Entries are either a `Memory` or, when `depth` collapses everything below a
        path, a `MemoryPrefix` standing in for that subtree.

        Args:
          memory_store_id: The memory store whose memories to list.

          limit: Maximum number of entries to return per page.

          page: Opaque page token from a previous response's `next_page`.

          depth: `1` collapses everything below `path_prefix` into `memory_prefix` entries.

          path_prefix: Restrict the listing to memories under this path.

          view: `full` includes each memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._get_api_list(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            page=SyncPageCursor[MemoryListItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "depth": depth,
                        "path_prefix": path_prefix,
                        "view": view,
                    },
                    memory_list_params.MemoryListParams,
                ),
            ),
            # Union types cannot be passed in as arguments in the type system.
            model=cast(Any, MemoryListItem),
        )

    def create(
        self,
        memory_store_id: str,
        *,
        path: str,
        content: Optional[str],
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Memory:
        """
        Create a memory at a path in a memory store.

        `view` is a query parameter that selects how much of the created memory comes
        back; only `path` and `content` are sent as the request body.

        Args:
          memory_store_id: The memory store to write into.

          path: Where the memory lives inside the store.

          content: Required, and explicitly nullable: pass `None` to create an empty memory.

          view: `full` returns the memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._post(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            body=maybe_transform(
                {"path": path, "content": content},
                memory_create_params.MemoryCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, memory_create_params.MemoryCreateQueryParams),
            ),
            cast_to=Memory,
        )

    def retrieve(
        self,
        memory_store_id: str,
        memory_id: str,
        *,
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Memory:
        """
        Retrieve a memory.

        Args:
          memory_store_id: The memory store holding the memory.

          memory_id: The memory to retrieve.

          view: `full` returns the memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return self._get(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, memory_retrieve_params.MemoryRetrieveParams),
            ),
            cast_to=Memory,
        )

    def update(
        self,
        memory_store_id: str,
        memory_id: str,
        *,
        content: Optional[str] | Omit = omit,
        path: Optional[str] | Omit = omit,
        precondition: MemoryContentSha256PreconditionParam | Omit = omit,
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Memory:
        """
        Partially update a memory.

        Uses POST, matching the contract. `view` is a query parameter; the remaining
        arguments form the request body. Pass `precondition` to opt into optimistic
        concurrency, so a concurrent write cannot be silently overwritten.

        Args:
          memory_store_id: The memory store holding the memory.

          memory_id: The memory to update.

          content: Replacement content.

          path: Moves the memory when set.

          precondition: Rejects the write unless the memory's content still hashes to the given value.

          view: `full` returns the memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return self._post(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            body=maybe_transform(
                {
                    "content": content,
                    "path": path,
                    "precondition": precondition,
                },
                memory_update_params.MemoryUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, memory_update_params.MemoryUpdateQueryParams),
            ),
            cast_to=Memory,
        )

    def delete(
        self,
        memory_store_id: str,
        memory_id: str,
        *,
        expected_content_sha256: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedMemory:
        """
        Delete a memory and return its tombstone.

        Args:
          memory_store_id: The memory store holding the memory.

          memory_id: The memory to delete.

          expected_content_sha256: Guard the delete: it is rejected unless the memory's content still hashes to
              this value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return self._delete(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"expected_content_sha256": expected_content_sha256},
                    memory_delete_params.MemoryDeleteParams,
                ),
            ),
            cast_to=DeletedMemory,
        )


class AsyncMemories(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMemoriesWithRawResponse:
        return AsyncMemoriesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemoriesWithStreamingResponse:
        return AsyncMemoriesWithStreamingResponse(self)

    def list(
        self,
        memory_store_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        depth: Optional[Literal[0, 1]] | Omit = omit,
        path_prefix: str | Omit = omit,
        view: MemoryView | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MemoryListItem, AsyncPageCursor[MemoryListItem]]:
        """
        List memories in a memory store.

        Entries are either a `Memory` or, when `depth` collapses everything below a
        path, a `MemoryPrefix` standing in for that subtree.

        Args:
          memory_store_id: The memory store whose memories to list.

          limit: Maximum number of entries to return per page.

          page: Opaque page token from a previous response's `next_page`.

          depth: `1` collapses everything below `path_prefix` into `memory_prefix` entries.

          path_prefix: Restrict the listing to memories under this path.

          view: `full` includes each memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._get_api_list(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            page=AsyncPageCursor[MemoryListItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "depth": depth,
                        "path_prefix": path_prefix,
                        "view": view,
                    },
                    memory_list_params.MemoryListParams,
                ),
            ),
            # Union types cannot be passed in as arguments in the type system.
            model=cast(Any, MemoryListItem),
        )

    async def create(
        self,
        memory_store_id: str,
        *,
        path: str,
        content: Optional[str],
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Memory:
        """
        Create a memory at a path in a memory store.

        `view` is a query parameter that selects how much of the created memory comes
        back; only `path` and `content` are sent as the request body.

        Args:
          memory_store_id: The memory store to write into.

          path: Where the memory lives inside the store.

          content: Required, and explicitly nullable: pass `None` to create an empty memory.

          view: `full` returns the memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return await self._post(
            path_template("/v1/memory_stores/{memory_store_id}/memories", memory_store_id=memory_store_id),
            body=await async_maybe_transform(
                {"path": path, "content": content},
                memory_create_params.MemoryCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, memory_create_params.MemoryCreateQueryParams),
            ),
            cast_to=Memory,
        )

    async def retrieve(
        self,
        memory_store_id: str,
        memory_id: str,
        *,
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Memory:
        """
        Retrieve a memory.

        Args:
          memory_store_id: The memory store holding the memory.

          memory_id: The memory to retrieve.

          view: `full` returns the memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return await self._get(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"view": view}, memory_retrieve_params.MemoryRetrieveParams),
            ),
            cast_to=Memory,
        )

    async def update(
        self,
        memory_store_id: str,
        memory_id: str,
        *,
        content: Optional[str] | Omit = omit,
        path: Optional[str] | Omit = omit,
        precondition: MemoryContentSha256PreconditionParam | Omit = omit,
        view: MemoryView | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Memory:
        """
        Partially update a memory.

        Uses POST, matching the contract. `view` is a query parameter; the remaining
        arguments form the request body. Pass `precondition` to opt into optimistic
        concurrency, so a concurrent write cannot be silently overwritten.

        Args:
          memory_store_id: The memory store holding the memory.

          memory_id: The memory to update.

          content: Replacement content.

          path: Moves the memory when set.

          precondition: Rejects the write unless the memory's content still hashes to the given value.

          view: `full` returns the memory's `content`; `basic` omits it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return await self._post(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            body=await async_maybe_transform(
                {
                    "content": content,
                    "path": path,
                    "precondition": precondition,
                },
                memory_update_params.MemoryUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"view": view}, memory_update_params.MemoryUpdateQueryParams),
            ),
            cast_to=Memory,
        )

    async def delete(
        self,
        memory_store_id: str,
        memory_id: str,
        *,
        expected_content_sha256: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedMemory:
        """
        Delete a memory and return its tombstone.

        Args:
          memory_store_id: The memory store holding the memory.

          memory_id: The memory to delete.

          expected_content_sha256: Guard the delete: it is rejected unless the memory's content still hashes to
              this value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return await self._delete(
            path_template(
                "/v1/memory_stores/{memory_store_id}/memories/{memory_id}",
                memory_store_id=memory_store_id,
                memory_id=memory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"expected_content_sha256": expected_content_sha256},
                    memory_delete_params.MemoryDeleteParams,
                ),
            ),
            cast_to=DeletedMemory,
        )


class MemoriesWithRawResponse:
    def __init__(self, memories: Memories) -> None:
        self._memories = memories

        self.list = to_raw_response_wrapper(memories.list)
        self.create = to_raw_response_wrapper(memories.create)
        self.retrieve = to_raw_response_wrapper(memories.retrieve)
        self.update = to_raw_response_wrapper(memories.update)
        self.delete = to_raw_response_wrapper(memories.delete)


class AsyncMemoriesWithRawResponse:
    def __init__(self, memories: AsyncMemories) -> None:
        self._memories = memories

        self.list = async_to_raw_response_wrapper(memories.list)
        self.create = async_to_raw_response_wrapper(memories.create)
        self.retrieve = async_to_raw_response_wrapper(memories.retrieve)
        self.update = async_to_raw_response_wrapper(memories.update)
        self.delete = async_to_raw_response_wrapper(memories.delete)


class MemoriesWithStreamingResponse:
    def __init__(self, memories: Memories) -> None:
        self._memories = memories

        self.list = to_streamed_response_wrapper(memories.list)
        self.create = to_streamed_response_wrapper(memories.create)
        self.retrieve = to_streamed_response_wrapper(memories.retrieve)
        self.update = to_streamed_response_wrapper(memories.update)
        self.delete = to_streamed_response_wrapper(memories.delete)


class AsyncMemoriesWithStreamingResponse:
    def __init__(self, memories: AsyncMemories) -> None:
        self._memories = memories

        self.list = async_to_streamed_response_wrapper(memories.list)
        self.create = async_to_streamed_response_wrapper(memories.create)
        self.retrieve = async_to_streamed_response_wrapper(memories.retrieve)
        self.update = async_to_streamed_response_wrapper(memories.update)
        self.delete = async_to_streamed_response_wrapper(memories.delete)
