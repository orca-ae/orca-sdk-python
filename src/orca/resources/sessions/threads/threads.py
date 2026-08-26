from __future__ import annotations

import httpx2

from .events import (
    ThreadEvents,
    AsyncThreadEvents,
    ThreadEventsWithRawResponse,
    AsyncThreadEventsWithRawResponse,
    ThreadEventsWithStreamingResponse,
    AsyncThreadEventsWithStreamingResponse,
)
from ....types import session_thread_list_params
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.session_thread import SessionThread

__all__ = ["Threads", "AsyncThreads"]


class Threads(SyncAPIResource):
    @cached_property
    def events(self) -> ThreadEvents:
        return ThreadEvents(self._client)

    @cached_property
    def with_raw_response(self) -> ThreadsWithRawResponse:
        return ThreadsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ThreadsWithStreamingResponse:
        return ThreadsWithStreamingResponse(self)

    def retrieve(
        self,
        session_id: str,
        thread_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionThread:
        """
        Retrieve one thread of a session.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._get(
            path_template("/v1/sessions/{session_id}/threads/{thread_id}", session_id=session_id, thread_id=thread_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionThread,
        )

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
    ) -> SyncPageCursor[SessionThread]:
        """
        List the threads of a session.

        A session always has a primary thread; child threads appear only once a
        coordinator agent spawns them. Threads are never created through the SDK.

        Args:
          session_id: The session whose threads to list.

          limit: Maximum number of threads to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/threads", session_id=session_id),
            page=SyncPageCursor[SessionThread],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    session_thread_list_params.SessionThreadListParams,
                ),
            ),
            model=SessionThread,
        )

    def archive(
        self,
        session_id: str,
        thread_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionThread:
        """
        Archive a thread and return it.

        Archiving stops the thread from running while keeping it retrievable by id.
        It is not a delete: thread deletion is not part of the portable surface.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._post(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/archive",
                session_id=session_id,
                thread_id=thread_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionThread,
        )


class AsyncThreads(AsyncAPIResource):
    @cached_property
    def events(self) -> AsyncThreadEvents:
        return AsyncThreadEvents(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncThreadsWithRawResponse:
        return AsyncThreadsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncThreadsWithStreamingResponse:
        return AsyncThreadsWithStreamingResponse(self)

    async def retrieve(
        self,
        session_id: str,
        thread_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionThread:
        """
        Retrieve one thread of a session.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._get(
            path_template("/v1/sessions/{session_id}/threads/{thread_id}", session_id=session_id, thread_id=thread_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionThread,
        )

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
    ) -> AsyncPaginator[SessionThread, AsyncPageCursor[SessionThread]]:
        """
        List the threads of a session.

        A session always has a primary thread; child threads appear only once a
        coordinator agent spawns them. Threads are never created through the SDK.

        Args:
          session_id: The session whose threads to list.

          limit: Maximum number of threads to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/threads", session_id=session_id),
            page=AsyncPageCursor[SessionThread],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    session_thread_list_params.SessionThreadListParams,
                ),
            ),
            model=SessionThread,
        )

    async def archive(
        self,
        session_id: str,
        thread_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionThread:
        """
        Archive a thread and return it.

        Archiving stops the thread from running while keeping it retrievable by id.
        It is not a delete: thread deletion is not part of the portable surface.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._post(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/archive",
                session_id=session_id,
                thread_id=thread_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionThread,
        )


class ThreadsWithRawResponse:
    def __init__(self, threads: Threads) -> None:
        self._threads = threads

        self.retrieve = to_raw_response_wrapper(threads.retrieve)
        self.list = to_raw_response_wrapper(threads.list)
        self.archive = to_raw_response_wrapper(threads.archive)

    @cached_property
    def events(self) -> ThreadEventsWithRawResponse:
        return ThreadEventsWithRawResponse(self._threads.events)


class AsyncThreadsWithRawResponse:
    def __init__(self, threads: AsyncThreads) -> None:
        self._threads = threads

        self.retrieve = async_to_raw_response_wrapper(threads.retrieve)
        self.list = async_to_raw_response_wrapper(threads.list)
        self.archive = async_to_raw_response_wrapper(threads.archive)

    @cached_property
    def events(self) -> AsyncThreadEventsWithRawResponse:
        return AsyncThreadEventsWithRawResponse(self._threads.events)


class ThreadsWithStreamingResponse:
    def __init__(self, threads: Threads) -> None:
        self._threads = threads

        self.retrieve = to_streamed_response_wrapper(threads.retrieve)
        self.list = to_streamed_response_wrapper(threads.list)
        self.archive = to_streamed_response_wrapper(threads.archive)

    @cached_property
    def events(self) -> ThreadEventsWithStreamingResponse:
        return ThreadEventsWithStreamingResponse(self._threads.events)


class AsyncThreadsWithStreamingResponse:
    def __init__(self, threads: AsyncThreads) -> None:
        self._threads = threads

        self.retrieve = async_to_streamed_response_wrapper(threads.retrieve)
        self.list = async_to_streamed_response_wrapper(threads.list)
        self.archive = async_to_streamed_response_wrapper(threads.archive)

    @cached_property
    def events(self) -> AsyncThreadEventsWithStreamingResponse:
        return AsyncThreadEventsWithStreamingResponse(self._threads.events)
