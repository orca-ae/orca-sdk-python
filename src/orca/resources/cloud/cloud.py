"""The `cloud.*` namespace router.

Operations served under `/apis/cloud.sn.io/v1/*` by the cloud extension service
rather than by the core engine. Every method reached through `client.cloud.*`
raises `ExtensionNotAvailableError` on a deployment that does not advertise the
`cloud.sn.io` group via `GET /apis` -- see `_gate.py`, which owns the group name
and the check.

`Cloud` itself issues no requests: it is a mount point, and each namespace below
it is imported inside its accessor rather than at module scope, exactly as
`_client.py` mounts its own resources. That keeps `import orca` from pulling in
eight extension namespaces a caller may never reach.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from .agents import (
        CloudAgents,
        AsyncCloudAgents,
        CloudAgentsWithRawResponse,
        AsyncCloudAgentsWithRawResponse,
        CloudAgentsWithStreamingResponse,
        AsyncCloudAgentsWithStreamingResponse,
    )
    from .health import (
        Health,
        AsyncHealth,
        HealthWithRawResponse,
        AsyncHealthWithRawResponse,
        HealthWithStreamingResponse,
        AsyncHealthWithStreamingResponse,
    )
    from .catalog import (
        Catalog,
        AsyncCatalog,
        CatalogWithRawResponse,
        AsyncCatalogWithRawResponse,
        CatalogWithStreamingResponse,
        AsyncCatalogWithStreamingResponse,
    )
    from .packages import (
        Packages,
        AsyncPackages,
        PackagesWithRawResponse,
        AsyncPackagesWithRawResponse,
        PackagesWithStreamingResponse,
        AsyncPackagesWithStreamingResponse,
    )
    from .functions import (
        Functions,
        AsyncFunctions,
        FunctionsWithRawResponse,
        AsyncFunctionsWithRawResponse,
        FunctionsWithStreamingResponse,
        AsyncFunctionsWithStreamingResponse,
    )
    from .connectors import (
        Connectors,
        AsyncConnectors,
        ConnectorsWithRawResponse,
        AsyncConnectorsWithRawResponse,
        ConnectorsWithStreamingResponse,
        AsyncConnectorsWithStreamingResponse,
    )
    from .connections import (
        Connections,
        AsyncConnections,
        ConnectionsWithRawResponse,
        AsyncConnectionsWithRawResponse,
        ConnectionsWithStreamingResponse,
        AsyncConnectionsWithStreamingResponse,
    )
    from .api_resources import (
        APIResources,
        AsyncAPIResources,
        APIResourcesWithRawResponse,
        AsyncAPIResourcesWithRawResponse,
        APIResourcesWithStreamingResponse,
        AsyncAPIResourcesWithStreamingResponse,
    )

__all__ = ["Cloud", "AsyncCloud"]


class Cloud(SyncAPIResource):
    @cached_property
    def api_resources(self) -> APIResources:
        from .api_resources import APIResources

        return APIResources(self._client)

    @cached_property
    def agents(self) -> CloudAgents:
        from .agents import CloudAgents

        return CloudAgents(self._client)

    @cached_property
    def catalog(self) -> Catalog:
        from .catalog import Catalog

        return Catalog(self._client)

    @cached_property
    def connections(self) -> Connections:
        from .connections import Connections

        return Connections(self._client)

    @cached_property
    def functions(self) -> Functions:
        from .functions import Functions

        return Functions(self._client)

    @cached_property
    def health(self) -> Health:
        from .health import Health

        return Health(self._client)

    @cached_property
    def packages(self) -> Packages:
        from .packages import Packages

        return Packages(self._client)

    @cached_property
    def connectors(self) -> Connectors:
        from .connectors import Connectors

        return Connectors(self._client)

    @cached_property
    def with_raw_response(self) -> CloudWithRawResponse:
        return CloudWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CloudWithStreamingResponse:
        return CloudWithStreamingResponse(self)


class AsyncCloud(AsyncAPIResource):
    @cached_property
    def api_resources(self) -> AsyncAPIResources:
        from .api_resources import AsyncAPIResources

        return AsyncAPIResources(self._client)

    @cached_property
    def agents(self) -> AsyncCloudAgents:
        from .agents import AsyncCloudAgents

        return AsyncCloudAgents(self._client)

    @cached_property
    def catalog(self) -> AsyncCatalog:
        from .catalog import AsyncCatalog

        return AsyncCatalog(self._client)

    @cached_property
    def connections(self) -> AsyncConnections:
        from .connections import AsyncConnections

        return AsyncConnections(self._client)

    @cached_property
    def functions(self) -> AsyncFunctions:
        from .functions import AsyncFunctions

        return AsyncFunctions(self._client)

    @cached_property
    def health(self) -> AsyncHealth:
        from .health import AsyncHealth

        return AsyncHealth(self._client)

    @cached_property
    def packages(self) -> AsyncPackages:
        from .packages import AsyncPackages

        return AsyncPackages(self._client)

    @cached_property
    def connectors(self) -> AsyncConnectors:
        from .connectors import AsyncConnectors

        return AsyncConnectors(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCloudWithRawResponse:
        return AsyncCloudWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCloudWithStreamingResponse:
        return AsyncCloudWithStreamingResponse(self)


class CloudWithRawResponse:
    def __init__(self, cloud: Cloud) -> None:
        self._cloud = cloud

    @cached_property
    def api_resources(self) -> APIResourcesWithRawResponse:
        from .api_resources import APIResourcesWithRawResponse

        return APIResourcesWithRawResponse(self._cloud.api_resources)

    @cached_property
    def agents(self) -> CloudAgentsWithRawResponse:
        from .agents import CloudAgentsWithRawResponse

        return CloudAgentsWithRawResponse(self._cloud.agents)

    @cached_property
    def catalog(self) -> CatalogWithRawResponse:
        from .catalog import CatalogWithRawResponse

        return CatalogWithRawResponse(self._cloud.catalog)

    @cached_property
    def connections(self) -> ConnectionsWithRawResponse:
        from .connections import ConnectionsWithRawResponse

        return ConnectionsWithRawResponse(self._cloud.connections)

    @cached_property
    def functions(self) -> FunctionsWithRawResponse:
        from .functions import FunctionsWithRawResponse

        return FunctionsWithRawResponse(self._cloud.functions)

    @cached_property
    def health(self) -> HealthWithRawResponse:
        from .health import HealthWithRawResponse

        return HealthWithRawResponse(self._cloud.health)

    @cached_property
    def packages(self) -> PackagesWithRawResponse:
        from .packages import PackagesWithRawResponse

        return PackagesWithRawResponse(self._cloud.packages)

    @cached_property
    def connectors(self) -> ConnectorsWithRawResponse:
        from .connectors import ConnectorsWithRawResponse

        return ConnectorsWithRawResponse(self._cloud.connectors)


class AsyncCloudWithRawResponse:
    def __init__(self, cloud: AsyncCloud) -> None:
        self._cloud = cloud

    @cached_property
    def api_resources(self) -> AsyncAPIResourcesWithRawResponse:
        from .api_resources import AsyncAPIResourcesWithRawResponse

        return AsyncAPIResourcesWithRawResponse(self._cloud.api_resources)

    @cached_property
    def agents(self) -> AsyncCloudAgentsWithRawResponse:
        from .agents import AsyncCloudAgentsWithRawResponse

        return AsyncCloudAgentsWithRawResponse(self._cloud.agents)

    @cached_property
    def catalog(self) -> AsyncCatalogWithRawResponse:
        from .catalog import AsyncCatalogWithRawResponse

        return AsyncCatalogWithRawResponse(self._cloud.catalog)

    @cached_property
    def connections(self) -> AsyncConnectionsWithRawResponse:
        from .connections import AsyncConnectionsWithRawResponse

        return AsyncConnectionsWithRawResponse(self._cloud.connections)

    @cached_property
    def functions(self) -> AsyncFunctionsWithRawResponse:
        from .functions import AsyncFunctionsWithRawResponse

        return AsyncFunctionsWithRawResponse(self._cloud.functions)

    @cached_property
    def health(self) -> AsyncHealthWithRawResponse:
        from .health import AsyncHealthWithRawResponse

        return AsyncHealthWithRawResponse(self._cloud.health)

    @cached_property
    def packages(self) -> AsyncPackagesWithRawResponse:
        from .packages import AsyncPackagesWithRawResponse

        return AsyncPackagesWithRawResponse(self._cloud.packages)

    @cached_property
    def connectors(self) -> AsyncConnectorsWithRawResponse:
        from .connectors import AsyncConnectorsWithRawResponse

        return AsyncConnectorsWithRawResponse(self._cloud.connectors)


class CloudWithStreamingResponse:
    def __init__(self, cloud: Cloud) -> None:
        self._cloud = cloud

    @cached_property
    def api_resources(self) -> APIResourcesWithStreamingResponse:
        from .api_resources import APIResourcesWithStreamingResponse

        return APIResourcesWithStreamingResponse(self._cloud.api_resources)

    @cached_property
    def agents(self) -> CloudAgentsWithStreamingResponse:
        from .agents import CloudAgentsWithStreamingResponse

        return CloudAgentsWithStreamingResponse(self._cloud.agents)

    @cached_property
    def catalog(self) -> CatalogWithStreamingResponse:
        from .catalog import CatalogWithStreamingResponse

        return CatalogWithStreamingResponse(self._cloud.catalog)

    @cached_property
    def connections(self) -> ConnectionsWithStreamingResponse:
        from .connections import ConnectionsWithStreamingResponse

        return ConnectionsWithStreamingResponse(self._cloud.connections)

    @cached_property
    def functions(self) -> FunctionsWithStreamingResponse:
        from .functions import FunctionsWithStreamingResponse

        return FunctionsWithStreamingResponse(self._cloud.functions)

    @cached_property
    def health(self) -> HealthWithStreamingResponse:
        from .health import HealthWithStreamingResponse

        return HealthWithStreamingResponse(self._cloud.health)

    @cached_property
    def packages(self) -> PackagesWithStreamingResponse:
        from .packages import PackagesWithStreamingResponse

        return PackagesWithStreamingResponse(self._cloud.packages)

    @cached_property
    def connectors(self) -> ConnectorsWithStreamingResponse:
        from .connectors import ConnectorsWithStreamingResponse

        return ConnectorsWithStreamingResponse(self._cloud.connectors)


class AsyncCloudWithStreamingResponse:
    def __init__(self, cloud: AsyncCloud) -> None:
        self._cloud = cloud

    @cached_property
    def api_resources(self) -> AsyncAPIResourcesWithStreamingResponse:
        from .api_resources import AsyncAPIResourcesWithStreamingResponse

        return AsyncAPIResourcesWithStreamingResponse(self._cloud.api_resources)

    @cached_property
    def agents(self) -> AsyncCloudAgentsWithStreamingResponse:
        from .agents import AsyncCloudAgentsWithStreamingResponse

        return AsyncCloudAgentsWithStreamingResponse(self._cloud.agents)

    @cached_property
    def catalog(self) -> AsyncCatalogWithStreamingResponse:
        from .catalog import AsyncCatalogWithStreamingResponse

        return AsyncCatalogWithStreamingResponse(self._cloud.catalog)

    @cached_property
    def connections(self) -> AsyncConnectionsWithStreamingResponse:
        from .connections import AsyncConnectionsWithStreamingResponse

        return AsyncConnectionsWithStreamingResponse(self._cloud.connections)

    @cached_property
    def functions(self) -> AsyncFunctionsWithStreamingResponse:
        from .functions import AsyncFunctionsWithStreamingResponse

        return AsyncFunctionsWithStreamingResponse(self._cloud.functions)

    @cached_property
    def health(self) -> AsyncHealthWithStreamingResponse:
        from .health import AsyncHealthWithStreamingResponse

        return AsyncHealthWithStreamingResponse(self._cloud.health)

    @cached_property
    def packages(self) -> AsyncPackagesWithStreamingResponse:
        from .packages import AsyncPackagesWithStreamingResponse

        return AsyncPackagesWithStreamingResponse(self._cloud.packages)

    @cached_property
    def connectors(self) -> AsyncConnectorsWithStreamingResponse:
        from .connectors import AsyncConnectorsWithStreamingResponse

        return AsyncConnectorsWithStreamingResponse(self._cloud.connectors)
