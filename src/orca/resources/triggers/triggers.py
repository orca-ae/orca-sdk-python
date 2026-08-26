from __future__ import annotations

import httpx2

from ...types import trigger_list_params, trigger_create_params, trigger_update_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from .sessions import (
    Sessions,
    AsyncSessions,
    SessionsWithRawResponse,
    AsyncSessionsWithRawResponse,
    SessionsWithStreamingResponse,
    AsyncSessionsWithStreamingResponse,
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
from ...types.trigger import Trigger, DeletedTrigger
from ...types.trigger_shared import (
    TriggerAgentParam,
    TriggerSessionMode,
    TriggerSourceCreateParam,
    TriggerSourceUpdateParam,
    TriggerSessionCreateParam,
    TriggerSessionUpdateParam,
)

__all__ = ["Triggers", "AsyncTriggers"]


class Triggers(SyncAPIResource):
    """Trigger lifecycle, shared by every supported deployment."""

    @cached_property
    def sessions(self) -> Sessions:
        return Sessions(self._client)

    @cached_property
    def with_raw_response(self) -> TriggersWithRawResponse:
        return TriggersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TriggersWithStreamingResponse:
        return TriggersWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        agent: TriggerAgentParam,
        session_mode: TriggerSessionMode,
        source: TriggerSourceCreateParam,
        session: TriggerSessionCreateParam,
        replicas: int | Omit = omit,
        paused: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Create a trigger.

        `session_mode` and `source` are deliberately not narrowed against each other:
        a `cron` source accepts only `SESSION_PER_EVENT` and `SHARED`, and a
        deployment that implements a narrower subset of sources or modes returns its
        own API error. The SDK does not preflight backend capabilities.

        Args:
          name: Human-readable name for the trigger.

          agent: The agent to run. A plain string is shorthand for `{"type": "agent", "id":
              <string>}`; the object form can pin a version.

          session_mode: How incoming events map onto sessions.

          source: What fires the trigger: a `cron` schedule, or a Kafka or Pulsar topic.

          session: Configuration for the sessions this trigger creates.

          replicas: Number of concurrent consumers. Positive; the server bounds the maximum.

          paused: Create the trigger already paused instead of active.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/triggers",
            body=maybe_transform(
                {
                    "name": name,
                    "agent": agent,
                    "session_mode": session_mode,
                    "source": source,
                    "session": session,
                    "replicas": replicas,
                    "paused": paused,
                },
                trigger_create_params.TriggerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        agent_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[Trigger]:
        """
        List triggers.

        Args:
          limit: Maximum number of triggers to return per page.

          page: Opaque page token from a previous response's `next_page`.

          agent_id: Only triggers that run this agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/triggers",
            page=SyncPageCursor[Trigger],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "agent_id": agent_id},
                    trigger_list_params.TriggerListParams,
                ),
            ),
            model=Trigger,
        )

    def retrieve(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Retrieve a trigger.

        Args:
          trigger_id: The trigger to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return self._get(
            path_template("/v1/triggers/{trigger_id}", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    def update(
        self,
        trigger_id: str,
        *,
        name: str | Omit = omit,
        session_mode: TriggerSessionMode | Omit = omit,
        source: TriggerSourceUpdateParam | Omit = omit,
        session: TriggerSessionUpdateParam | Omit = omit,
        replicas: int | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Partially update a trigger.

        Uses POST, matching the contract. A `source` patch still carries its `type`
        discriminator, which selects the variant being patched rather than changing
        the source kind.

        Args:
          trigger_id: The trigger to update.

          session_mode: How incoming events map onto sessions.

          source: Fields to change on the existing source; unset fields are preserved.

          session: Fields to change on the session configuration. A null metadata value removes
              that individual key.

          replicas: Number of concurrent consumers. Positive; the server bounds the maximum.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return self._post(
            path_template("/v1/triggers/{trigger_id}", trigger_id=trigger_id),
            body=maybe_transform(
                {
                    "name": name,
                    "session_mode": session_mode,
                    "source": source,
                    "session": session,
                    "replicas": replicas,
                },
                trigger_update_params.TriggerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedTrigger:
        """
        Permanently delete a trigger and return its tombstone.

        Use `pause` to stop a trigger firing while keeping its configuration.

        Args:
          trigger_id: The trigger to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return self._delete(
            path_template("/v1/triggers/{trigger_id}", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedTrigger,
        )

    def pause(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Pause a trigger and return it.

        The trigger stops firing but keeps its configuration; `unpause` resumes it.

        Args:
          trigger_id: The trigger to pause.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return self._post(
            path_template("/v1/triggers/{trigger_id}/pause", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    def unpause(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Resume a paused trigger and return it.

        Args:
          trigger_id: The trigger to resume.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return self._post(
            path_template("/v1/triggers/{trigger_id}/unpause", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )


class AsyncTriggers(AsyncAPIResource):
    """Trigger lifecycle, shared by every supported deployment."""

    @cached_property
    def sessions(self) -> AsyncSessions:
        return AsyncSessions(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTriggersWithRawResponse:
        return AsyncTriggersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTriggersWithStreamingResponse:
        return AsyncTriggersWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        agent: TriggerAgentParam,
        session_mode: TriggerSessionMode,
        source: TriggerSourceCreateParam,
        session: TriggerSessionCreateParam,
        replicas: int | Omit = omit,
        paused: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Create a trigger.

        `session_mode` and `source` are deliberately not narrowed against each other:
        a `cron` source accepts only `SESSION_PER_EVENT` and `SHARED`, and a
        deployment that implements a narrower subset of sources or modes returns its
        own API error. The SDK does not preflight backend capabilities.

        Args:
          name: Human-readable name for the trigger.

          agent: The agent to run. A plain string is shorthand for `{"type": "agent", "id":
              <string>}`; the object form can pin a version.

          session_mode: How incoming events map onto sessions.

          source: What fires the trigger: a `cron` schedule, or a Kafka or Pulsar topic.

          session: Configuration for the sessions this trigger creates.

          replicas: Number of concurrent consumers. Positive; the server bounds the maximum.

          paused: Create the trigger already paused instead of active.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/triggers",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "agent": agent,
                    "session_mode": session_mode,
                    "source": source,
                    "session": session,
                    "replicas": replicas,
                    "paused": paused,
                },
                trigger_create_params.TriggerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        agent_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Trigger, AsyncPageCursor[Trigger]]:
        """
        List triggers.

        Args:
          limit: Maximum number of triggers to return per page.

          page: Opaque page token from a previous response's `next_page`.

          agent_id: Only triggers that run this agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/triggers",
            page=AsyncPageCursor[Trigger],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "agent_id": agent_id},
                    trigger_list_params.TriggerListParams,
                ),
            ),
            model=Trigger,
        )

    async def retrieve(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Retrieve a trigger.

        Args:
          trigger_id: The trigger to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return await self._get(
            path_template("/v1/triggers/{trigger_id}", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    async def update(
        self,
        trigger_id: str,
        *,
        name: str | Omit = omit,
        session_mode: TriggerSessionMode | Omit = omit,
        source: TriggerSourceUpdateParam | Omit = omit,
        session: TriggerSessionUpdateParam | Omit = omit,
        replicas: int | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Partially update a trigger.

        Uses POST, matching the contract. A `source` patch still carries its `type`
        discriminator, which selects the variant being patched rather than changing
        the source kind.

        Args:
          trigger_id: The trigger to update.

          session_mode: How incoming events map onto sessions.

          source: Fields to change on the existing source; unset fields are preserved.

          session: Fields to change on the session configuration. A null metadata value removes
              that individual key.

          replicas: Number of concurrent consumers. Positive; the server bounds the maximum.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return await self._post(
            path_template("/v1/triggers/{trigger_id}", trigger_id=trigger_id),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "session_mode": session_mode,
                    "source": source,
                    "session": session,
                    "replicas": replicas,
                },
                trigger_update_params.TriggerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    async def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedTrigger:
        """
        Permanently delete a trigger and return its tombstone.

        Use `pause` to stop a trigger firing while keeping its configuration.

        Args:
          trigger_id: The trigger to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return await self._delete(
            path_template("/v1/triggers/{trigger_id}", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedTrigger,
        )

    async def pause(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Pause a trigger and return it.

        The trigger stops firing but keeps its configuration; `unpause` resumes it.

        Args:
          trigger_id: The trigger to pause.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return await self._post(
            path_template("/v1/triggers/{trigger_id}/pause", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )

    async def unpause(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Trigger:
        """
        Resume a paused trigger and return it.

        Args:
          trigger_id: The trigger to resume.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trigger_id:
            raise ValueError(f"Expected a non-empty value for `trigger_id` but received {trigger_id!r}")
        return await self._post(
            path_template("/v1/triggers/{trigger_id}/unpause", trigger_id=trigger_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Trigger,
        )


class TriggersWithRawResponse:
    def __init__(self, triggers: Triggers) -> None:
        self._triggers = triggers

        self.create = to_raw_response_wrapper(triggers.create)
        self.list = to_raw_response_wrapper(triggers.list)
        self.retrieve = to_raw_response_wrapper(triggers.retrieve)
        self.update = to_raw_response_wrapper(triggers.update)
        self.delete = to_raw_response_wrapper(triggers.delete)
        self.pause = to_raw_response_wrapper(triggers.pause)
        self.unpause = to_raw_response_wrapper(triggers.unpause)

    @cached_property
    def sessions(self) -> SessionsWithRawResponse:
        return SessionsWithRawResponse(self._triggers.sessions)


class AsyncTriggersWithRawResponse:
    def __init__(self, triggers: AsyncTriggers) -> None:
        self._triggers = triggers

        self.create = async_to_raw_response_wrapper(triggers.create)
        self.list = async_to_raw_response_wrapper(triggers.list)
        self.retrieve = async_to_raw_response_wrapper(triggers.retrieve)
        self.update = async_to_raw_response_wrapper(triggers.update)
        self.delete = async_to_raw_response_wrapper(triggers.delete)
        self.pause = async_to_raw_response_wrapper(triggers.pause)
        self.unpause = async_to_raw_response_wrapper(triggers.unpause)

    @cached_property
    def sessions(self) -> AsyncSessionsWithRawResponse:
        return AsyncSessionsWithRawResponse(self._triggers.sessions)


class TriggersWithStreamingResponse:
    def __init__(self, triggers: Triggers) -> None:
        self._triggers = triggers

        self.create = to_streamed_response_wrapper(triggers.create)
        self.list = to_streamed_response_wrapper(triggers.list)
        self.retrieve = to_streamed_response_wrapper(triggers.retrieve)
        self.update = to_streamed_response_wrapper(triggers.update)
        self.delete = to_streamed_response_wrapper(triggers.delete)
        self.pause = to_streamed_response_wrapper(triggers.pause)
        self.unpause = to_streamed_response_wrapper(triggers.unpause)

    @cached_property
    def sessions(self) -> SessionsWithStreamingResponse:
        return SessionsWithStreamingResponse(self._triggers.sessions)


class AsyncTriggersWithStreamingResponse:
    def __init__(self, triggers: AsyncTriggers) -> None:
        self._triggers = triggers

        self.create = async_to_streamed_response_wrapper(triggers.create)
        self.list = async_to_streamed_response_wrapper(triggers.list)
        self.retrieve = async_to_streamed_response_wrapper(triggers.retrieve)
        self.update = async_to_streamed_response_wrapper(triggers.update)
        self.delete = async_to_streamed_response_wrapper(triggers.delete)
        self.pause = async_to_streamed_response_wrapper(triggers.pause)
        self.unpause = async_to_streamed_response_wrapper(triggers.unpause)

    @cached_property
    def sessions(self) -> AsyncSessionsWithStreamingResponse:
        return AsyncSessionsWithStreamingResponse(self._triggers.sessions)
