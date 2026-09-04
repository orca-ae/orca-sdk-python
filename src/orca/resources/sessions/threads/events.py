from __future__ import annotations

from typing import List, Union

import httpx2

from ....types import (
    session_thread_event_list_params,
    session_thread_event_stream_params,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._streaming import Stream, AsyncStream
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.session_event import SessionEvent
from ....types.session_event_stream_params import SessionEventDelta

__all__ = ["ThreadEvents", "AsyncThreadEvents"]


class ThreadEvents(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ThreadEventsWithRawResponse:
        return ThreadEventsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ThreadEventsWithStreamingResponse:
        return ThreadEventsWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        thread_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[SessionEvent]:
        """
        List the events recorded on one thread.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread whose events to list.

          limit: Maximum number of events to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._get_api_list(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/events",
                session_id=session_id,
                thread_id=thread_id,
            ),
            page=SyncPageCursor[SessionEvent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    session_thread_event_list_params.SessionThreadEventListParams,
                ),
            ),
            model=SessionEvent,
        )

    def stream(
        self,
        session_id: str,
        thread_id: str,
        *,
        from_cursor: str | Omit = omit,
        event_deltas: Union[SessionEventDelta, List[SessionEventDelta]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Stream[SessionEvent]:
        """
        Open a server-sent-event stream for one thread.

        The thread stream hangs off `/threads/{thread_id}/stream`, not
        `/threads/{thread_id}/events/stream`; that is what the contract defines.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread to stream.

          from_cursor: Resume after this event id instead of starting at the live edge.

          event_deltas: Event types to receive as incremental deltas rather than only when complete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
        return self._get(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/stream",
                session_id=session_id,
                thread_id=thread_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"from_cursor": from_cursor, "event_deltas": event_deltas},
                    session_thread_event_stream_params.SessionThreadEventStreamParams,
                ),
            ),
            cast_to=SessionEvent,
            stream=True,
            stream_cls=Stream[SessionEvent],
        )


class AsyncThreadEvents(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncThreadEventsWithRawResponse:
        return AsyncThreadEventsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncThreadEventsWithStreamingResponse:
        return AsyncThreadEventsWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        thread_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SessionEvent, AsyncPageCursor[SessionEvent]]:
        """
        List the events recorded on one thread.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread whose events to list.

          limit: Maximum number of events to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._get_api_list(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/events",
                session_id=session_id,
                thread_id=thread_id,
            ),
            page=AsyncPageCursor[SessionEvent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    session_thread_event_list_params.SessionThreadEventListParams,
                ),
            ),
            model=SessionEvent,
        )

    async def stream(
        self,
        session_id: str,
        thread_id: str,
        *,
        from_cursor: str | Omit = omit,
        event_deltas: Union[SessionEventDelta, List[SessionEventDelta]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[SessionEvent]:
        """
        Open a server-sent-event stream for one thread.

        The thread stream hangs off `/threads/{thread_id}/stream`, not
        `/threads/{thread_id}/events/stream`; that is what the contract defines.

        Args:
          session_id: The session that owns the thread.

          thread_id: The thread to stream.

          from_cursor: Resume after this event id instead of starting at the live edge.

          event_deltas: Event types to receive as incremental deltas rather than only when complete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/stream",
                session_id=session_id,
                thread_id=thread_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"from_cursor": from_cursor, "event_deltas": event_deltas},
                    session_thread_event_stream_params.SessionThreadEventStreamParams,
                ),
            ),
            cast_to=SessionEvent,
            stream=True,
            stream_cls=AsyncStream[SessionEvent],
        )


class ThreadEventsWithRawResponse:
    def __init__(self, events: ThreadEvents) -> None:
        self._events = events

        self.list = to_raw_response_wrapper(events.list)
        self.stream = to_raw_response_wrapper(events.stream)


class AsyncThreadEventsWithRawResponse:
    def __init__(self, events: AsyncThreadEvents) -> None:
        self._events = events

        self.list = async_to_raw_response_wrapper(events.list)
        self.stream = async_to_raw_response_wrapper(events.stream)


class ThreadEventsWithStreamingResponse:
    def __init__(self, events: ThreadEvents) -> None:
        self._events = events

        self.list = to_streamed_response_wrapper(events.list)
        self.stream = to_streamed_response_wrapper(events.stream)


class AsyncThreadEventsWithStreamingResponse:
    def __init__(self, events: AsyncThreadEvents) -> None:
        self._events = events

        self.list = async_to_streamed_response_wrapper(events.list)
        self.stream = async_to_streamed_response_wrapper(events.stream)
