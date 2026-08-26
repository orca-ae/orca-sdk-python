from __future__ import annotations

from typing import Dict, List, Union, Optional

import httpx2

from ...types import agent_list_params, agent_create_params, agent_update_params, agent_retrieve_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from .versions import (
    Versions,
    AsyncVersions,
    VersionsWithRawResponse,
    AsyncVersionsWithRawResponse,
    VersionsWithStreamingResponse,
    AsyncVersionsWithStreamingResponse,
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
from ...types.agent import Agent
from ..._base_client import AsyncPaginator, make_request_options
from ...types.agent_shared import (
    ModelConfigParam,
    AgentMcpServerParam,
    AgentToolDefinitionParam,
    AgentSkillDefinitionParam,
    AgentMultiagentDefinitionParam,
)

__all__ = ["Agents", "AsyncAgents"]


class Agents(SyncAPIResource):
    @cached_property
    def versions(self) -> Versions:
        return Versions(self._client)

    @cached_property
    def with_raw_response(self) -> AgentsWithRawResponse:
        return AgentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentsWithStreamingResponse:
        return AgentsWithStreamingResponse(self)

    def create(
        self,
        *,
        model: Union[str, ModelConfigParam],
        name: str,
        description: Optional[str] | Omit = omit,
        system: Optional[str] | Omit = omit,
        mcp_servers: List[AgentMcpServerParam] | Omit = omit,
        tools: List[AgentToolDefinitionParam] | Omit = omit,
        skills: List[AgentSkillDefinitionParam] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        multiagent: Optional[AgentMultiagentDefinitionParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Create an agent.

        Args:
          model: Model to use. A plain string is shorthand for `{"id": <string>}`.

          name: Human-readable name for the agent.

          description: Free-text description.

          system: System prompt.

          mcp_servers: MCP servers the agent may reach.

          tools: Tool definitions available to the agent.

          skills: Skills attached to the agent.

          metadata: Arbitrary string key/value pairs.

          multiagent: Coordinator configuration when this agent orchestrates others.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/agents",
            body=maybe_transform(
                {
                    "model": model,
                    "name": name,
                    "description": description,
                    "system": system,
                    "mcp_servers": mcp_servers,
                    "tools": tools,
                    "skills": skills,
                    "metadata": metadata,
                    "multiagent": multiagent,
                },
                agent_create_params.AgentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )

    def retrieve(
        self,
        agent_id: str,
        *,
        version: int | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Retrieve an agent.

        Args:
          agent_id: The agent to retrieve.

          version: Retrieve a specific historical version rather than the current one.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._get(
            path_template("/v1/agents/{agent_id}", agent_id=agent_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"version": version}, agent_retrieve_params.AgentRetrieveParams),
            ),
            cast_to=Agent,
        )

    def update(
        self,
        agent_id: str,
        *,
        version: int | Omit = omit,
        name: str | Omit = omit,
        description: Optional[str] | Omit = omit,
        model: Union[str, ModelConfigParam] | Omit = omit,
        system: Optional[str] | Omit = omit,
        mcp_servers: Optional[List[AgentMcpServerParam]] | Omit = omit,
        tools: Optional[List[AgentToolDefinitionParam]] | Omit = omit,
        skills: Optional[List[AgentSkillDefinitionParam]] | Omit = omit,
        multiagent: Optional[AgentMultiagentDefinitionParam] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Partially update an agent.

        Uses POST, matching the contract. Pass `version` to opt into optimistic
        concurrency: the write is rejected unless it matches the agent's current
        version, so a concurrent update cannot be silently overwritten.

        Args:
          agent_id: The agent to update.

          version: Must match the agent's current version when provided.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            path_template("/v1/agents/{agent_id}", agent_id=agent_id),
            body=maybe_transform(
                {
                    "version": version,
                    "name": name,
                    "description": description,
                    "model": model,
                    "system": system,
                    "mcp_servers": mcp_servers,
                    "tools": tools,
                    "skills": skills,
                    "multiagent": multiagent,
                    "metadata": metadata,
                },
                agent_update_params.AgentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
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
    ) -> SyncPageCursor[Agent]:
        """
        List agents.

        Args:
          limit: Maximum number of agents to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived agents in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/agents",
            page=SyncPageCursor[Agent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    agent_list_params.AgentListParams,
                ),
            ),
            model=Agent,
        )

    def archive(
        self,
        agent_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Archive an agent and return it.

        Archiving hides the agent from default listings while keeping it and its
        version history retrievable by id. It is not a delete: agent deletion is not
        part of the portable surface.

        Args:
          agent_id: The agent to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            path_template("/v1/agents/{agent_id}/archive", agent_id=agent_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )


class AsyncAgents(AsyncAPIResource):
    @cached_property
    def versions(self) -> AsyncVersions:
        return AsyncVersions(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAgentsWithRawResponse:
        return AsyncAgentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentsWithStreamingResponse:
        return AsyncAgentsWithStreamingResponse(self)

    async def create(
        self,
        *,
        model: Union[str, ModelConfigParam],
        name: str,
        description: Optional[str] | Omit = omit,
        system: Optional[str] | Omit = omit,
        mcp_servers: List[AgentMcpServerParam] | Omit = omit,
        tools: List[AgentToolDefinitionParam] | Omit = omit,
        skills: List[AgentSkillDefinitionParam] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        multiagent: Optional[AgentMultiagentDefinitionParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Create an agent.

        Args:
          model: Model to use. A plain string is shorthand for `{"id": <string>}`.

          name: Human-readable name for the agent.

          description: Free-text description.

          system: System prompt.

          mcp_servers: MCP servers the agent may reach.

          tools: Tool definitions available to the agent.

          skills: Skills attached to the agent.

          metadata: Arbitrary string key/value pairs.

          multiagent: Coordinator configuration when this agent orchestrates others.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/agents",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "name": name,
                    "description": description,
                    "system": system,
                    "mcp_servers": mcp_servers,
                    "tools": tools,
                    "skills": skills,
                    "metadata": metadata,
                    "multiagent": multiagent,
                },
                agent_create_params.AgentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )

    async def retrieve(
        self,
        agent_id: str,
        *,
        version: int | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Retrieve an agent.

        Args:
          agent_id: The agent to retrieve.

          version: Retrieve a specific historical version rather than the current one.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._get(
            path_template("/v1/agents/{agent_id}", agent_id=agent_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"version": version}, agent_retrieve_params.AgentRetrieveParams),
            ),
            cast_to=Agent,
        )

    async def update(
        self,
        agent_id: str,
        *,
        version: int | Omit = omit,
        name: str | Omit = omit,
        description: Optional[str] | Omit = omit,
        model: Union[str, ModelConfigParam] | Omit = omit,
        system: Optional[str] | Omit = omit,
        mcp_servers: Optional[List[AgentMcpServerParam]] | Omit = omit,
        tools: Optional[List[AgentToolDefinitionParam]] | Omit = omit,
        skills: Optional[List[AgentSkillDefinitionParam]] | Omit = omit,
        multiagent: Optional[AgentMultiagentDefinitionParam] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Partially update an agent.

        Uses POST, matching the contract. Pass `version` to opt into optimistic
        concurrency: the write is rejected unless it matches the agent's current
        version, so a concurrent update cannot be silently overwritten.

        Args:
          agent_id: The agent to update.

          version: Must match the agent's current version when provided.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            path_template("/v1/agents/{agent_id}", agent_id=agent_id),
            body=await async_maybe_transform(
                {
                    "version": version,
                    "name": name,
                    "description": description,
                    "model": model,
                    "system": system,
                    "mcp_servers": mcp_servers,
                    "tools": tools,
                    "skills": skills,
                    "multiagent": multiagent,
                    "metadata": metadata,
                },
                agent_update_params.AgentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
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
    ) -> AsyncPaginator[Agent, AsyncPageCursor[Agent]]:
        """
        List agents.

        Args:
          limit: Maximum number of agents to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived agents in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/agents",
            page=AsyncPageCursor[Agent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    agent_list_params.AgentListParams,
                ),
            ),
            model=Agent,
        )

    async def archive(
        self,
        agent_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Archive an agent and return it.

        Archiving hides the agent from default listings while keeping it and its
        version history retrievable by id. It is not a delete: agent deletion is not
        part of the portable surface.

        Args:
          agent_id: The agent to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            path_template("/v1/agents/{agent_id}/archive", agent_id=agent_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )


class AgentsWithRawResponse:
    def __init__(self, agents: Agents) -> None:
        self._agents = agents

        self.create = to_raw_response_wrapper(agents.create)
        self.retrieve = to_raw_response_wrapper(agents.retrieve)
        self.update = to_raw_response_wrapper(agents.update)
        self.list = to_raw_response_wrapper(agents.list)
        self.archive = to_raw_response_wrapper(agents.archive)

    @cached_property
    def versions(self) -> VersionsWithRawResponse:
        return VersionsWithRawResponse(self._agents.versions)


class AsyncAgentsWithRawResponse:
    def __init__(self, agents: AsyncAgents) -> None:
        self._agents = agents

        self.create = async_to_raw_response_wrapper(agents.create)
        self.retrieve = async_to_raw_response_wrapper(agents.retrieve)
        self.update = async_to_raw_response_wrapper(agents.update)
        self.list = async_to_raw_response_wrapper(agents.list)
        self.archive = async_to_raw_response_wrapper(agents.archive)

    @cached_property
    def versions(self) -> AsyncVersionsWithRawResponse:
        return AsyncVersionsWithRawResponse(self._agents.versions)


class AgentsWithStreamingResponse:
    def __init__(self, agents: Agents) -> None:
        self._agents = agents

        self.create = to_streamed_response_wrapper(agents.create)
        self.retrieve = to_streamed_response_wrapper(agents.retrieve)
        self.update = to_streamed_response_wrapper(agents.update)
        self.list = to_streamed_response_wrapper(agents.list)
        self.archive = to_streamed_response_wrapper(agents.archive)

    @cached_property
    def versions(self) -> VersionsWithStreamingResponse:
        return VersionsWithStreamingResponse(self._agents.versions)


class AsyncAgentsWithStreamingResponse:
    def __init__(self, agents: AsyncAgents) -> None:
        self._agents = agents

        self.create = async_to_streamed_response_wrapper(agents.create)
        self.retrieve = async_to_streamed_response_wrapper(agents.retrieve)
        self.update = async_to_streamed_response_wrapper(agents.update)
        self.list = async_to_streamed_response_wrapper(agents.list)
        self.archive = async_to_streamed_response_wrapper(agents.archive)

    @cached_property
    def versions(self) -> AsyncVersionsWithStreamingResponse:
        return AsyncVersionsWithStreamingResponse(self._agents.versions)
