from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AgentRetrieveParams"]


class AgentRetrieveParams(TypedDict, total=False):
    version: int
    """Retrieve a specific historical version rather than the current one."""
