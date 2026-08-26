from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .memory import MemoryView

__all__ = ["MemoryCreateParams", "MemoryCreateQueryParams"]


class MemoryCreateParams(TypedDict, total=False):
    """The request body. `view` is a query parameter, not a body field."""

    path: Required[str]

    content: Required[Optional[str]]
    """Required, and explicitly nullable: pass `None` to create an empty memory."""


class MemoryCreateQueryParams(TypedDict, total=False):
    view: MemoryView
