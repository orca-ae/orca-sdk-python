from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["MemoryStore", "DeletedMemoryStore"]


class MemoryStore(BaseModel):
    """A named container for agent memories, scoped to a workspace.

    Attach a store to a session through that session's `resources` to mount it as a
    directory the agent can read from and write to.
    """

    id: str

    type: Literal["memory_store"]

    name: str

    description: Optional[str] = None

    metadata: Optional[Dict[str, str]] = None

    created_at: str

    updated_at: str

    archived_at: Optional[str] = None
    """Present but null while the store is active."""


class DeletedMemoryStore(BaseModel):
    id: str

    type: Literal["memory_store_deleted"]
