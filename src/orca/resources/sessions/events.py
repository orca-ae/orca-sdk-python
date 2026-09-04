from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal

import httpx2

from ...types import (
    session_event_list_params,
    session_event_send_params,
    session_event_stream_params,
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
from ..._streaming import Stream, AsyncStream
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.session_event import SessionEvent, SessionEventInputParam
from ...types.session_event_send_response import SessionEventSendResponse
from ...types.session_event_stream_params import SessionEventDelta

__all__ = ["Events", "AsyncEvents"]


class Events(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventsWithRawResponse:
        return EventsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventsWithStreamingResponse:
        return EventsWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        created_at_gt: str | Omit = omit,
        created_at_gte: str | Omit = omit,
        created_at_lt: str | Omit = omit,
        created_at_lte: str | Omit = omit,
        order: Literal["asc", "desc"] | Omit = omit,
        types: Union[str, List[str]] | Omit = omit,
        subpath: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[SessionEvent]:
        """
        List the events persisted for a session.

        Args:
          session_id: The session whose events to list.

          limit: Maximum number of events to return per page.

          page: Opaque page token from a previous response's `next_page`.

          created_at_gt: Sent as `created_at[gt]`.

          created_at_gte: Sent as `created_at[gte]`.

          created_at_lt: Sent as `created_at[lt]`.

          created_at_lte: Sent as `created_at[lte]`.

          order: `asc` or `desc` by creation time.

          types: One event type or a list of them.

          subpath: Restrict to events recorded under a sub-agent path.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/events", session_id=session_id),
            page=SyncPageCursor[SessionEvent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "created_at_gt": created_at_gt,
                        "created_at_gte": created_at_gte,
                        "created_at_lt": created_at_lt,
                        "created_at_lte": created_at_lte,
                        "order": order,
                        "types": types,
                        "subpath": subpath,
                    },
                    session_event_list_params.SessionEventListParams,
                ),
            ),
            model=SessionEvent,
        )

    def send(
        self,
        session_id: str,
        *,
        events: List[SessionEventInputParam],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionEventSendResponse:
        """
        Append one or more events to a session.

        Args:
          session_id: The session to append to.

          events: Events to append, in order.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            path_template("/v1/sessions/{session_id}/events", session_id=session_id),
            body=maybe_transform({"events": events}, session_event_send_params.SessionEventSendParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionEventSendResponse,
        )

    def stream(
        self,
        session_id: str,
        *,
        from_cursor: str | Omit = omit,
        subpath: str | Omit = omit,
        event_deltas: Union[SessionEventDelta, List[SessionEventDelta]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Stream[SessionEvent]:
        """
        Open a server-sent-event stream of a session's events.

        Pass `from_cursor` to resume: the stream replays everything after that event
        id before following the live edge, so a dropped connection loses no events.

        Args:
          session_id: The session to stream.

          from_cursor: Resume after this event id instead of starting at the live edge.

          subpath: Restrict to events recorded under a sub-agent path.

          event_deltas: Event types to receive as incremental deltas rather than only when complete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
        return self._get(
            path_template("/v1/sessions/{session_id}/events/stream", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "from_cursor": from_cursor,
                        "subpath": subpath,
                        "event_deltas": event_deltas,
                    },
                    session_event_stream_params.SessionEventStreamParams,
                ),
            ),
            cast_to=SessionEvent,
            stream=True,
            stream_cls=Stream[SessionEvent],
        )


class AsyncEvents(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventsWithRawResponse:
        return AsyncEventsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventsWithStreamingResponse:
        return AsyncEventsWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        created_at_gt: str | Omit = omit,
        created_at_gte: str | Omit = omit,
        created_at_lt: str | Omit = omit,
        created_at_lte: str | Omit = omit,
        order: Literal["asc", "desc"] | Omit = omit,
        types: Union[str, List[str]] | Omit = omit,
        subpath: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SessionEvent, AsyncPageCursor[SessionEvent]]:
        """
        List the events persisted for a session.

        Args:
          session_id: The session whose events to list.

          limit: Maximum number of events to return per page.

          page: Opaque page token from a previous response's `next_page`.

          created_at_gt: Sent as `created_at[gt]`.

          created_at_gte: Sent as `created_at[gte]`.

          created_at_lt: Sent as `created_at[lt]`.

          created_at_lte: Sent as `created_at[lte]`.

          order: `asc` or `desc` by creation time.

          types: One event type or a list of them.

          subpath: Restrict to events recorded under a sub-agent path.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/events", session_id=session_id),
            page=AsyncPageCursor[SessionEvent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "created_at_gt": created_at_gt,
                        "created_at_gte": created_at_gte,
                        "created_at_lt": created_at_lt,
                        "created_at_lte": created_at_lte,
                        "order": order,
                        "types": types,
                        "subpath": subpath,
                    },
                    session_event_list_params.SessionEventListParams,
                ),
            ),
            model=SessionEvent,
        )

    async def send(
        self,
        session_id: str,
        *,
        events: List[SessionEventInputParam],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionEventSendResponse:
        """
        Append one or more events to a session.

        Args:
          session_id: The session to append to.

          events: Events to append, in order.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            path_template("/v1/sessions/{session_id}/events", session_id=session_id),
            body=await async_maybe_transform({"events": events}, session_event_send_params.SessionEventSendParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionEventSendResponse,
        )

    async def stream(
        self,
        session_id: str,
        *,
        from_cursor: str | Omit = omit,
        subpath: str | Omit = omit,
        event_deltas: Union[SessionEventDelta, List[SessionEventDelta]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[SessionEvent]:
        """
        Open a server-sent-event stream of a session's events.

        Pass `from_cursor` to resume: the stream replays everything after that event
        id before following the live edge, so a dropped connection loses no events.

        Args:
          session_id: The session to stream.

          from_cursor: Resume after this event id instead of starting at the live edge.

          subpath: Restrict to events recorded under a sub-agent path.

          event_deltas: Event types to receive as incremental deltas rather than only when complete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/sessions/{session_id}/events/stream", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "from_cursor": from_cursor,
                        "subpath": subpath,
                        "event_deltas": event_deltas,
                    },
                    session_event_stream_params.SessionEventStreamParams,
                ),
            ),
            cast_to=SessionEvent,
            stream=True,
            stream_cls=AsyncStream[SessionEvent],
        )


class EventsWithRawResponse:
    def __init__(self, events: Events) -> None:
        self._events = events

        self.list = to_raw_response_wrapper(events.list)
        self.send = to_raw_response_wrapper(events.send)
        self.stream = to_raw_response_wrapper(events.stream)


class AsyncEventsWithRawResponse:
    def __init__(self, events: AsyncEvents) -> None:
        self._events = events

        self.list = async_to_raw_response_wrapper(events.list)
        self.send = async_to_raw_response_wrapper(events.send)
        self.stream = async_to_raw_response_wrapper(events.stream)


class EventsWithStreamingResponse:
    def __init__(self, events: Events) -> None:
        self._events = events

        self.list = to_streamed_response_wrapper(events.list)
        self.send = to_streamed_response_wrapper(events.send)
        self.stream = to_streamed_response_wrapper(events.stream)


class AsyncEventsWithStreamingResponse:
    def __init__(self, events: AsyncEvents) -> None:
        self._events = events

        self.list = async_to_streamed_response_wrapper(events.list)
        self.send = async_to_streamed_response_wrapper(events.send)
        self.stream = async_to_streamed_response_wrapper(events.stream)
