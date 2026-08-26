from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

from .memory import MemoryView

__all__ = ["MemoryListParams"]


class MemoryListParams(TypedDict, total=False):
    limit: int

    page: str
    """Opaque page token from a previous response's `next_page`."""

    depth: Optional[Literal[0, 1]]
    """`1` collapses everything below `path_prefix` into `memory_prefix` entries."""

    path_prefix: str

    view: MemoryView
