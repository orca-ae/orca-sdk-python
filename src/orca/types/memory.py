from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["MemoryView", "Memory", "MemoryPrefix", "MemoryListItem", "DeletedMemory"]

MemoryView: TypeAlias = Literal["basic", "full"]
"""How much of a memory to return. `full` includes `content`; `basic` omits it."""


class Memory(BaseModel):
    id: str

    content_sha256: str

    content_size_bytes: int

    created_at: str

    memory_store_id: str

    memory_version_id: str
    """The version this memory's current content came from."""

    path: str

    type: Literal["memory"]

    updated_at: str

    content: Optional[str] = None
    """Only returned for the `full` view."""


class MemoryPrefix(BaseModel):
    """A directory-like grouping returned when a list is limited by `depth`."""

    path: str

    type: Literal["memory_prefix"]


MemoryListItem: TypeAlias = Union[Memory, MemoryPrefix]


class DeletedMemory(BaseModel):
    id: str

    type: Literal["memory_deleted"]
