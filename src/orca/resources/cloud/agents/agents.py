from __future__ import annotations

from .providers import (
    Providers,
    AsyncProviders,
    ProvidersWithRawResponse,
    AsyncProvidersWithRawResponse,
    ProvidersWithStreamingResponse,
    AsyncProvidersWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["CloudAgents", "AsyncCloudAgents"]


class CloudAgents(SyncAPIResource):
    """Agent operations only the cloud extension serves.

    Mounted at `client.cloud.agents`, alongside -- not instead of -- core
    `client.agents`. A router only; it has no operations of its own.
    """

    @cached_property
    def providers(self) -> Providers:
        return Providers(self._client)

    @cached_property
    def with_raw_response(self) -> CloudAgentsWithRawResponse:
        return CloudAgentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CloudAgentsWithStreamingResponse:
        return CloudAgentsWithStreamingResponse(self)


class AsyncCloudAgents(AsyncAPIResource):
    """Agent operations only the cloud extension serves.

    Mounted at `client.cloud.agents`, alongside -- not instead of -- core
    `client.agents`. A router only; it has no operations of its own.
    """

    @cached_property
    def providers(self) -> AsyncProviders:
        return AsyncProviders(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCloudAgentsWithRawResponse:
        return AsyncCloudAgentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCloudAgentsWithStreamingResponse:
        return AsyncCloudAgentsWithStreamingResponse(self)


class CloudAgentsWithRawResponse:
    def __init__(self, cloud_agents: CloudAgents) -> None:
        self._cloud_agents = cloud_agents

    @cached_property
    def providers(self) -> ProvidersWithRawResponse:
        return ProvidersWithRawResponse(self._cloud_agents.providers)


class AsyncCloudAgentsWithRawResponse:
    def __init__(self, cloud_agents: AsyncCloudAgents) -> None:
        self._cloud_agents = cloud_agents

    @cached_property
    def providers(self) -> AsyncProvidersWithRawResponse:
        return AsyncProvidersWithRawResponse(self._cloud_agents.providers)


class CloudAgentsWithStreamingResponse:
    def __init__(self, cloud_agents: CloudAgents) -> None:
        self._cloud_agents = cloud_agents

    @cached_property
    def providers(self) -> ProvidersWithStreamingResponse:
        return ProvidersWithStreamingResponse(self._cloud_agents.providers)


class AsyncCloudAgentsWithStreamingResponse:
    def __init__(self, cloud_agents: AsyncCloudAgents) -> None:
        self._cloud_agents = cloud_agents

    @cached_property
    def providers(self) -> AsyncProvidersWithStreamingResponse:
        return AsyncProvidersWithStreamingResponse(self._cloud_agents.providers)
