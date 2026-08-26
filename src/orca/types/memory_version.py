from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "MemoryVersionOperation",
    "MemoryVersionSessionActor",
    "MemoryVersionAPIActor",
    "MemoryVersionUserActor",
    "MemoryVersionActor",
    "MemoryVersion",
]

MemoryVersionOperation: TypeAlias = Literal["created", "modified", "deleted"]


class MemoryVersionSessionActor(BaseModel):
    type: Literal["session_actor"]

    session_id: str


class MemoryVersionAPIActor(BaseModel):
    type: Literal["api_actor"]

    api_key_id: str


class MemoryVersionUserActor(BaseModel):
    type: Literal["user_actor"]

    user_id: str


MemoryVersionActor: TypeAlias = Union[MemoryVersionSessionActor, MemoryVersionAPIActor, MemoryVersionUserActor]


class MemoryVersion(BaseModel):
    """One entry in a memory store's audit trail."""

    id: str

    created_at: str

    memory_id: str

    memory_store_id: str

    operation: MemoryVersionOperation

    type: Literal["memory_version"]

    content: Optional[str] = None
    """Only returned for the `full` view, and null once the version is redacted."""

    content_sha256: Optional[str] = None

    content_size_bytes: Optional[int] = None

    created_by: Optional[MemoryVersionActor] = None

    path: Optional[str] = None

    redacted_at: Optional[str] = None
    """Set once the version's content has been redacted."""

    redacted_by: Optional[MemoryVersionActor] = None
