from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .memory import MemoryView

__all__ = ["MemoryUpdateParams", "MemoryUpdateQueryParams", "MemoryContentSha256PreconditionParam"]


class MemoryContentSha256PreconditionParam(TypedDict, total=False):
    type: Required[Literal["content_sha256"]]

    content_sha256: str
    """The hash the memory must currently have for the write to be applied."""


class MemoryUpdateParams(TypedDict, total=False):
    """The request body. `view` is a query parameter, not a body field."""

    content: Optional[str]

    path: Optional[str]
    """Moves the memory when set."""

    precondition: MemoryContentSha256PreconditionParam
    """Opt into optimistic concurrency: the write is rejected unless the memory's
    current content still hashes to `content_sha256`, so a concurrent write cannot
    be silently overwritten."""


class MemoryUpdateQueryParams(TypedDict, total=False):
    view: MemoryView
