"""Shared capability gate for extension API groups."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from .._client import Orca, AsyncOrca

__all__ = ["extension_gate", "async_extension_gate"]


def extension_gate(resource: SyncAPIResource, group: str) -> None:
    """Raise before the business request unless the deployment advertises `group`."""
    cast("Orca", resource._client)._ensure_extension_available(group)


async def async_extension_gate(resource: AsyncAPIResource, group: str) -> None:
    """Async counterpart to `extension_gate`."""
    await cast("AsyncOrca", resource._client)._ensure_extension_available(group)
