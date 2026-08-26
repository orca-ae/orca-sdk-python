from __future__ import annotations

from typing import Optional

import httpx2

from ...types import trigger_session_list_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform
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

__all__ = ["Sessions", "AsyncSessions"]

# Page items are core `Session` entities. They are typed as `object` here until the
# shared session model lands in `types/`; this narrows to that model once it does.


class Sessions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SessionsWithRawResponse:
        return SessionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionsWithStreamingResponse:
        return SessionsWithStreamingResponse(self)

    def list(
        self,
        trigger_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[object]:
        """
        List the sessions a trigger created.

        Args:
          trigger_id: The trigger whose sessions to list.

          limit: Maximum number of sessions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived sessions in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return self._get_api_list(
            path_template("/v1/triggers/{trigger_id}/sessions", trigger_id=trigger_id),
            page=SyncPageCursor[object],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    trigger_session_list_params.TriggerSessionListParams,
                ),
            ),
            model=object,
        )


class AsyncSessions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSessionsWithRawResponse:
        return AsyncSessionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionsWithStreamingResponse:
        return AsyncSessionsWithStreamingResponse(self)

    def list(
        self,
        trigger_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[object, AsyncPageCursor[object]]:
        """
        List the sessions a trigger created.

        Args:
          trigger_id: The trigger whose sessions to list.

          limit: Maximum number of sessions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived sessions in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return self._get_api_list(
            path_template("/v1/triggers/{trigger_id}/sessions", trigger_id=trigger_id),
            page=AsyncPageCursor[object],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    trigger_session_list_params.TriggerSessionListParams,
                ),
            ),
            model=object,
        )


class SessionsWithRawResponse:
    def __init__(self, sessions: Sessions) -> None:
        self._sessions = sessions

        self.list = to_raw_response_wrapper(sessions.list)


class AsyncSessionsWithRawResponse:
    def __init__(self, sessions: AsyncSessions) -> None:
        self._sessions = sessions

        self.list = async_to_raw_response_wrapper(sessions.list)


class SessionsWithStreamingResponse:
    def __init__(self, sessions: Sessions) -> None:
        self._sessions = sessions

        self.list = to_streamed_response_wrapper(sessions.list)


class AsyncSessionsWithStreamingResponse:
    def __init__(self, sessions: AsyncSessions) -> None:
        self._sessions = sessions

        self.list = async_to_streamed_response_wrapper(sessions.list)
