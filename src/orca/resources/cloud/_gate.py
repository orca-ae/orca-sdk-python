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

from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._constants import CLOUD_EXTENSION_GROUP
from .._extension_gate import extension_gate, async_extension_gate

__all__ = ["CLOUD_EXTENSION_GROUP", "cloud_gate", "async_cloud_gate"]


def cloud_gate(resource: SyncAPIResource) -> None:
    """Raise `ExtensionNotAvailableError` unless this deployment serves `cloud.sn.io`.

    `SyncAPIResource` types `_client` as the transport base class; the narrowing lives
    here so call sites stay a single readable line.
    """
    extension_gate(resource, CLOUD_EXTENSION_GROUP)


async def async_cloud_gate(resource: AsyncAPIResource) -> None:
    """Raise `ExtensionNotAvailableError` unless this deployment serves `cloud.sn.io`."""
    await async_extension_gate(resource, CLOUD_EXTENSION_GROUP)
