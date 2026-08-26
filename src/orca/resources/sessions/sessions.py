from __future__ import annotations

from typing import Dict, List, Optional

import httpx2

from .files import (
    SessionFiles,
    AsyncSessionFiles,
    SessionFilesWithRawResponse,
    AsyncSessionFilesWithRawResponse,
    SessionFilesWithStreamingResponse,
    AsyncSessionFilesWithStreamingResponse,
)
from .events import (
    Events,
    AsyncEvents,
    EventsWithRawResponse,
    AsyncEventsWithRawResponse,
    EventsWithStreamingResponse,
    AsyncEventsWithStreamingResponse,
)
from ...types import session_list_params, session_create_params, session_update_params
from .threads import (
    Threads,
    AsyncThreads,
    ThreadsWithRawResponse,
    AsyncThreadsWithRawResponse,
    ThreadsWithStreamingResponse,
    AsyncThreadsWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .resources import (
    Resources,
    AsyncResources,
    ResourcesWithRawResponse,
    AsyncResourcesWithRawResponse,
    ResourcesWithStreamingResponse,
    AsyncResourcesWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.session import Session, DeletedSession
from ...types.session_resource import SessionResourceRequestParam
from ...types.session_create_params import SessionAgentInputParam, SessionInitialEventParam
from ...types.session_update_params import SessionAgentUpdateParam

__all__ = ["Sessions", "AsyncSessions"]


class Sessions(SyncAPIResource):
    @cached_property
    def events(self) -> Events:
        return Events(self._client)

    @cached_property
    def files(self) -> SessionFiles:
        return SessionFiles(self._client)

    @cached_property
    def resources(self) -> Resources:
        return Resources(self._client)

    @cached_property
    def threads(self) -> Threads:
        return Threads(self._client)

    @cached_property
    def with_raw_response(self) -> SessionsWithRawResponse:
        return SessionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionsWithStreamingResponse:
        return SessionsWithStreamingResponse(self)

    def create(
        self,
        *,
        environment_id: str,
        agent: SessionAgentInputParam | Omit = omit,
        agent_id: str | Omit = omit,
        vault_ids: List[str] | Omit = omit,
        title: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        resources: List[SessionResourceRequestParam] | Omit = omit,
        initial_events: List[SessionInitialEventParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Create a session.

        Args:
          environment_id: Environment the session runs in.

          agent: Agent reference. A plain string is shorthand for `{"id": <string>}`. Pass either
              this or `agent_id`, not both.

          agent_id: Compatibility form of the agent reference accepted by both backends.

          vault_ids: Vaults whose credentials the session may read.

          title: Human-readable title.

          metadata: Arbitrary string key/value pairs.

          resources: Files, repositories, and memory stores mounted into the session.

          initial_events: Events applied before the agent's first turn.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/sessions",
            body=maybe_transform(
                {
                    "environment_id": environment_id,
                    "agent": agent,
                    "agent_id": agent_id,
                    "vault_ids": vault_ids,
                    "title": title,
                    "metadata": metadata,
                    "resources": resources,
                    "initial_events": initial_events,
                },
                session_create_params.SessionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )

    def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Retrieve a session.

        Args:
          session_id: The session to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get(
            path_template("/v1/sessions/{session_id}", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )

    def update(
        self,
        session_id: str,
        *,
        agent: SessionAgentUpdateParam | Omit = omit,
        vault_ids: List[str] | Omit = omit,
        title: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Partially update a session.

        Uses POST, matching the contract. The `agent` field edits the session's frozen
        agent snapshot in place; it does not repoint the session at another agent.

        Args:
          session_id: The session to update.

          agent: Narrow edits to the session's agent snapshot.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            path_template("/v1/sessions/{session_id}", session_id=session_id),
            body=maybe_transform(
                {
                    "agent": agent,
                    "vault_ids": vault_ids,
                    "title": title,
                    "metadata": metadata,
                },
                session_update_params.SessionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )

    def list(
        self,
        *,
        agent_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: Optional[bool] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[Session]:
        """
        List sessions.

        Args:
          agent_id: Filter to sessions owned by one agent.

          limit: Maximum number of sessions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived sessions in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/sessions",
            page=SyncPageCursor[Session],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "limit": limit,
                        "page": page,
                        "include_archived": include_archived,
                    },
                    session_list_params.SessionListParams,
                ),
            ),
            model=Session,
        )

    def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSession:
        """
        Permanently delete a session and return its tombstone.

        Unlike agents, sessions really can be deleted. Use `archive` to keep the
        session retrievable while hiding it from default listings.

        Args:
          session_id: The session to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._delete(
            path_template("/v1/sessions/{session_id}", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSession,
        )

    def archive(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Archive a session and return it.

        Archiving hides the session from default listings while keeping it, its
        events, and its threads retrievable by id.

        Args:
          session_id: The session to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            path_template("/v1/sessions/{session_id}/archive", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )


class AsyncSessions(AsyncAPIResource):
    @cached_property
    def events(self) -> AsyncEvents:
        return AsyncEvents(self._client)

    @cached_property
    def files(self) -> AsyncSessionFiles:
        return AsyncSessionFiles(self._client)

    @cached_property
    def resources(self) -> AsyncResources:
        return AsyncResources(self._client)

    @cached_property
    def threads(self) -> AsyncThreads:
        return AsyncThreads(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSessionsWithRawResponse:
        return AsyncSessionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionsWithStreamingResponse:
        return AsyncSessionsWithStreamingResponse(self)

    async def create(
        self,
        *,
        environment_id: str,
        agent: SessionAgentInputParam | Omit = omit,
        agent_id: str | Omit = omit,
        vault_ids: List[str] | Omit = omit,
        title: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        resources: List[SessionResourceRequestParam] | Omit = omit,
        initial_events: List[SessionInitialEventParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Create a session.

        Args:
          environment_id: Environment the session runs in.

          agent: Agent reference. A plain string is shorthand for `{"id": <string>}`. Pass either
              this or `agent_id`, not both.

          agent_id: Compatibility form of the agent reference accepted by both backends.

          vault_ids: Vaults whose credentials the session may read.

          title: Human-readable title.

          metadata: Arbitrary string key/value pairs.

          resources: Files, repositories, and memory stores mounted into the session.

          initial_events: Events applied before the agent's first turn.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/sessions",
            body=await async_maybe_transform(
                {
                    "environment_id": environment_id,
                    "agent": agent,
                    "agent_id": agent_id,
                    "vault_ids": vault_ids,
                    "title": title,
                    "metadata": metadata,
                    "resources": resources,
                    "initial_events": initial_events,
                },
                session_create_params.SessionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )

    async def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Retrieve a session.

        Args:
          session_id: The session to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._get(
            path_template("/v1/sessions/{session_id}", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )

    async def update(
        self,
        session_id: str,
        *,
        agent: SessionAgentUpdateParam | Omit = omit,
        vault_ids: List[str] | Omit = omit,
        title: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Partially update a session.

        Uses POST, matching the contract. The `agent` field edits the session's frozen
        agent snapshot in place; it does not repoint the session at another agent.

        Args:
          session_id: The session to update.

          agent: Narrow edits to the session's agent snapshot.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            path_template("/v1/sessions/{session_id}", session_id=session_id),
            body=await async_maybe_transform(
                {
                    "agent": agent,
                    "vault_ids": vault_ids,
                    "title": title,
                    "metadata": metadata,
                },
                session_update_params.SessionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )

    def list(
        self,
        *,
        agent_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: Optional[bool] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Session, AsyncPageCursor[Session]]:
        """
        List sessions.

        Args:
          agent_id: Filter to sessions owned by one agent.

          limit: Maximum number of sessions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived sessions in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/sessions",
            page=AsyncPageCursor[Session],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "limit": limit,
                        "page": page,
                        "include_archived": include_archived,
                    },
                    session_list_params.SessionListParams,
                ),
            ),
            model=Session,
        )

    async def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSession:
        """
        Permanently delete a session and return its tombstone.

        Unlike agents, sessions really can be deleted. Use `archive` to keep the
        session retrievable while hiding it from default listings.

        Args:
          session_id: The session to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._delete(
            path_template("/v1/sessions/{session_id}", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSession,
        )

    async def archive(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Session:
        """
        Archive a session and return it.

        Archiving hides the session from default listings while keeping it, its
        events, and its threads retrievable by id.

        Args:
          session_id: The session to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            path_template("/v1/sessions/{session_id}/archive", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
        )


class SessionsWithRawResponse:
    def __init__(self, sessions: Sessions) -> None:
        self._sessions = sessions

        self.create = to_raw_response_wrapper(sessions.create)
        self.retrieve = to_raw_response_wrapper(sessions.retrieve)
        self.update = to_raw_response_wrapper(sessions.update)
        self.list = to_raw_response_wrapper(sessions.list)
        self.delete = to_raw_response_wrapper(sessions.delete)
        self.archive = to_raw_response_wrapper(sessions.archive)

    @cached_property
    def events(self) -> EventsWithRawResponse:
        return EventsWithRawResponse(self._sessions.events)

    @cached_property
    def files(self) -> SessionFilesWithRawResponse:
        return SessionFilesWithRawResponse(self._sessions.files)

    @cached_property
    def resources(self) -> ResourcesWithRawResponse:
        return ResourcesWithRawResponse(self._sessions.resources)

    @cached_property
    def threads(self) -> ThreadsWithRawResponse:
        return ThreadsWithRawResponse(self._sessions.threads)


class AsyncSessionsWithRawResponse:
    def __init__(self, sessions: AsyncSessions) -> None:
        self._sessions = sessions

        self.create = async_to_raw_response_wrapper(sessions.create)
        self.retrieve = async_to_raw_response_wrapper(sessions.retrieve)
        self.update = async_to_raw_response_wrapper(sessions.update)
        self.list = async_to_raw_response_wrapper(sessions.list)
        self.delete = async_to_raw_response_wrapper(sessions.delete)
        self.archive = async_to_raw_response_wrapper(sessions.archive)

    @cached_property
    def events(self) -> AsyncEventsWithRawResponse:
        return AsyncEventsWithRawResponse(self._sessions.events)

    @cached_property
    def files(self) -> AsyncSessionFilesWithRawResponse:
        return AsyncSessionFilesWithRawResponse(self._sessions.files)

    @cached_property
    def resources(self) -> AsyncResourcesWithRawResponse:
        return AsyncResourcesWithRawResponse(self._sessions.resources)

    @cached_property
    def threads(self) -> AsyncThreadsWithRawResponse:
        return AsyncThreadsWithRawResponse(self._sessions.threads)


class SessionsWithStreamingResponse:
    def __init__(self, sessions: Sessions) -> None:
        self._sessions = sessions

        self.create = to_streamed_response_wrapper(sessions.create)
        self.retrieve = to_streamed_response_wrapper(sessions.retrieve)
        self.update = to_streamed_response_wrapper(sessions.update)
        self.list = to_streamed_response_wrapper(sessions.list)
        self.delete = to_streamed_response_wrapper(sessions.delete)
        self.archive = to_streamed_response_wrapper(sessions.archive)

    @cached_property
    def events(self) -> EventsWithStreamingResponse:
        return EventsWithStreamingResponse(self._sessions.events)

    @cached_property
    def files(self) -> SessionFilesWithStreamingResponse:
        return SessionFilesWithStreamingResponse(self._sessions.files)

    @cached_property
    def resources(self) -> ResourcesWithStreamingResponse:
        return ResourcesWithStreamingResponse(self._sessions.resources)

    @cached_property
    def threads(self) -> ThreadsWithStreamingResponse:
        return ThreadsWithStreamingResponse(self._sessions.threads)


class AsyncSessionsWithStreamingResponse:
    def __init__(self, sessions: AsyncSessions) -> None:
        self._sessions = sessions

        self.create = async_to_streamed_response_wrapper(sessions.create)
        self.retrieve = async_to_streamed_response_wrapper(sessions.retrieve)
        self.update = async_to_streamed_response_wrapper(sessions.update)
        self.list = async_to_streamed_response_wrapper(sessions.list)
        self.delete = async_to_streamed_response_wrapper(sessions.delete)
        self.archive = async_to_streamed_response_wrapper(sessions.archive)

    @cached_property
    def events(self) -> AsyncEventsWithStreamingResponse:
        return AsyncEventsWithStreamingResponse(self._sessions.events)

    @cached_property
    def files(self) -> AsyncSessionFilesWithStreamingResponse:
        return AsyncSessionFilesWithStreamingResponse(self._sessions.files)

    @cached_property
    def resources(self) -> AsyncResourcesWithStreamingResponse:
        return AsyncResourcesWithStreamingResponse(self._sessions.resources)

    @cached_property
    def threads(self) -> AsyncThreadsWithStreamingResponse:
        return AsyncThreadsWithStreamingResponse(self._sessions.threads)
