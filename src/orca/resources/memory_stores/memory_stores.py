from __future__ import annotations

from typing import Dict, Optional

import httpx2

from ...types import memory_store_list_params, memory_store_create_params, memory_store_update_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from .memories import (
    Memories,
    AsyncMemories,
    MemoriesWithRawResponse,
    AsyncMemoriesWithRawResponse,
    MemoriesWithStreamingResponse,
    AsyncMemoriesWithStreamingResponse,
)
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
from .memory_versions import (
    MemoryVersions,
    AsyncMemoryVersions,
    MemoryVersionsWithRawResponse,
    AsyncMemoryVersionsWithRawResponse,
    MemoryVersionsWithStreamingResponse,
    AsyncMemoryVersionsWithStreamingResponse,
)
from ...types.memory_store import MemoryStore, DeletedMemoryStore

__all__ = ["MemoryStores", "AsyncMemoryStores"]


class MemoryStores(SyncAPIResource):
    @cached_property
    def memories(self) -> Memories:
        return Memories(self._client)

    @cached_property
    def memory_versions(self) -> MemoryVersions:
        return MemoryVersions(self._client)

    @cached_property
    def with_raw_response(self) -> MemoryStoresWithRawResponse:
        return MemoryStoresWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemoryStoresWithStreamingResponse:
        return MemoryStoresWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Create a memory store.

        Args:
          name: Human-readable name; 1-255 characters.

          description: Free-text description, up to 1024 characters.

          metadata: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/memory_stores",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                },
                memory_store_create_params.MemoryStoreCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )

    def retrieve(
        self,
        memory_store_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Retrieve a memory store.

        Args:
          memory_store_id: The memory store to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._get(
            path_template("/v1/memory_stores/{memory_store_id}", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )

    def update(
        self,
        memory_store_id: str,
        *,
        name: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Partially update a memory store.

        Uses POST, matching the contract.

        Args:
          memory_store_id: The memory store to update.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._post(
            path_template("/v1/memory_stores/{memory_store_id}", memory_store_id=memory_store_id),
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                },
                memory_store_update_params.MemoryStoreUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[MemoryStore]:
        """
        List memory stores.

        Args:
          limit: Maximum number of memory stores to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived memory stores in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/memory_stores",
            page=SyncPageCursor[MemoryStore],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    memory_store_list_params.MemoryStoreListParams,
                ),
            ),
            model=MemoryStore,
        )

    def delete(
        self,
        memory_store_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedMemoryStore:
        """
        Permanently delete a memory store and return its tombstone.

        This removes the store and its memories for good. Use `archive` to hide a
        store from default listings while keeping it retrievable by id.

        Args:
          memory_store_id: The memory store to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._delete(
            path_template("/v1/memory_stores/{memory_store_id}", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedMemoryStore,
        )

    def archive(
        self,
        memory_store_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Archive a memory store and return it.

        Archiving hides the store from default listings while keeping it and its
        memories retrievable by id. `delete` is the permanent counterpart.

        Args:
          memory_store_id: The memory store to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return self._post(
            path_template("/v1/memory_stores/{memory_store_id}/archive", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )


class AsyncMemoryStores(AsyncAPIResource):
    @cached_property
    def memories(self) -> AsyncMemories:
        return AsyncMemories(self._client)

    @cached_property
    def memory_versions(self) -> AsyncMemoryVersions:
        return AsyncMemoryVersions(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMemoryStoresWithRawResponse:
        return AsyncMemoryStoresWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemoryStoresWithStreamingResponse:
        return AsyncMemoryStoresWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Create a memory store.

        Args:
          name: Human-readable name; 1-255 characters.

          description: Free-text description, up to 1024 characters.

          metadata: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/memory_stores",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                },
                memory_store_create_params.MemoryStoreCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )

    async def retrieve(
        self,
        memory_store_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Retrieve a memory store.

        Args:
          memory_store_id: The memory store to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return await self._get(
            path_template("/v1/memory_stores/{memory_store_id}", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )

    async def update(
        self,
        memory_store_id: str,
        *,
        name: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Partially update a memory store.

        Uses POST, matching the contract.

        Args:
          memory_store_id: The memory store to update.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return await self._post(
            path_template("/v1/memory_stores/{memory_store_id}", memory_store_id=memory_store_id),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                },
                memory_store_update_params.MemoryStoreUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MemoryStore, AsyncPageCursor[MemoryStore]]:
        """
        List memory stores.

        Args:
          limit: Maximum number of memory stores to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived memory stores in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/memory_stores",
            page=AsyncPageCursor[MemoryStore],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    memory_store_list_params.MemoryStoreListParams,
                ),
            ),
            model=MemoryStore,
        )

    async def delete(
        self,
        memory_store_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedMemoryStore:
        """
        Permanently delete a memory store and return its tombstone.

        This removes the store and its memories for good. Use `archive` to hide a
        store from default listings while keeping it retrievable by id.

        Args:
          memory_store_id: The memory store to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return await self._delete(
            path_template("/v1/memory_stores/{memory_store_id}", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedMemoryStore,
        )

    async def archive(
        self,
        memory_store_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemoryStore:
        """
        Archive a memory store and return it.

        Archiving hides the store from default listings while keeping it and its
        memories retrievable by id. `delete` is the permanent counterpart.

        Args:
          memory_store_id: The memory store to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_store_id:
            raise ValueError(f"Expected a non-empty value for `memory_store_id` but received {memory_store_id!r}")
        return await self._post(
            path_template("/v1/memory_stores/{memory_store_id}/archive", memory_store_id=memory_store_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryStore,
        )


class MemoryStoresWithRawResponse:
    def __init__(self, memory_stores: MemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = to_raw_response_wrapper(memory_stores.create)
        self.retrieve = to_raw_response_wrapper(memory_stores.retrieve)
        self.update = to_raw_response_wrapper(memory_stores.update)
        self.list = to_raw_response_wrapper(memory_stores.list)
        self.delete = to_raw_response_wrapper(memory_stores.delete)
        self.archive = to_raw_response_wrapper(memory_stores.archive)

    @cached_property
    def memories(self) -> MemoriesWithRawResponse:
        return MemoriesWithRawResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> MemoryVersionsWithRawResponse:
        return MemoryVersionsWithRawResponse(self._memory_stores.memory_versions)


class AsyncMemoryStoresWithRawResponse:
    def __init__(self, memory_stores: AsyncMemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = async_to_raw_response_wrapper(memory_stores.create)
        self.retrieve = async_to_raw_response_wrapper(memory_stores.retrieve)
        self.update = async_to_raw_response_wrapper(memory_stores.update)
        self.list = async_to_raw_response_wrapper(memory_stores.list)
        self.delete = async_to_raw_response_wrapper(memory_stores.delete)
        self.archive = async_to_raw_response_wrapper(memory_stores.archive)

    @cached_property
    def memories(self) -> AsyncMemoriesWithRawResponse:
        return AsyncMemoriesWithRawResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> AsyncMemoryVersionsWithRawResponse:
        return AsyncMemoryVersionsWithRawResponse(self._memory_stores.memory_versions)


class MemoryStoresWithStreamingResponse:
    def __init__(self, memory_stores: MemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = to_streamed_response_wrapper(memory_stores.create)
        self.retrieve = to_streamed_response_wrapper(memory_stores.retrieve)
        self.update = to_streamed_response_wrapper(memory_stores.update)
        self.list = to_streamed_response_wrapper(memory_stores.list)
        self.delete = to_streamed_response_wrapper(memory_stores.delete)
        self.archive = to_streamed_response_wrapper(memory_stores.archive)

    @cached_property
    def memories(self) -> MemoriesWithStreamingResponse:
        return MemoriesWithStreamingResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> MemoryVersionsWithStreamingResponse:
        return MemoryVersionsWithStreamingResponse(self._memory_stores.memory_versions)


class AsyncMemoryStoresWithStreamingResponse:
    def __init__(self, memory_stores: AsyncMemoryStores) -> None:
        self._memory_stores = memory_stores

        self.create = async_to_streamed_response_wrapper(memory_stores.create)
        self.retrieve = async_to_streamed_response_wrapper(memory_stores.retrieve)
        self.update = async_to_streamed_response_wrapper(memory_stores.update)
        self.list = async_to_streamed_response_wrapper(memory_stores.list)
        self.delete = async_to_streamed_response_wrapper(memory_stores.delete)
        self.archive = async_to_streamed_response_wrapper(memory_stores.archive)

    @cached_property
    def memories(self) -> AsyncMemoriesWithStreamingResponse:
        return AsyncMemoriesWithStreamingResponse(self._memory_stores.memories)

    @cached_property
    def memory_versions(self) -> AsyncMemoryVersionsWithStreamingResponse:
        return AsyncMemoryVersionsWithStreamingResponse(self._memory_stores.memory_versions)
