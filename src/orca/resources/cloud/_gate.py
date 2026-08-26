"""Extension gating for the `cloud.*` namespace.

Every method under `client.cloud` confirms the deployment advertises the
`cloud.sn.io` extension group before issuing its request. A deployment that does not
serve the group -- a self-hosted engine, for instance -- produces
`ExtensionNotAvailableError`, and no HTTP call is made for the gated operation.

The TypeScript client gates by handing the request pipeline a *promise* of request
options. The synchronous Python client has no equivalent, so the gate is an explicit
call at the top of each method instead. Discovery is cached per base URL, so only the
first gated call on a client pays for it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Orca, AsyncOrca

CLOUD_EXTENSION_GROUP = "cloud.sn.io"

__all__ = ["CLOUD_EXTENSION_GROUP", "cloud_gate", "async_cloud_gate"]


def cloud_gate(resource: SyncAPIResource) -> None:
    """Raise `ExtensionNotAvailableError` unless this deployment serves `cloud.sn.io`.

    `SyncAPIResource` types `_client` as the transport base class; the narrowing lives
    here so call sites stay a single readable line.
    """
    cast("Orca", resource._client)._ensure_extension_available(CLOUD_EXTENSION_GROUP)


async def async_cloud_gate(resource: AsyncAPIResource) -> None:
    """Raise `ExtensionNotAvailableError` unless this deployment serves `cloud.sn.io`."""
    await cast("AsyncOrca", resource._client)._ensure_extension_available(CLOUD_EXTENSION_GROUP)
