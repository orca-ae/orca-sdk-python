from __future__ import annotations

from typing_extensions import TypedDict

from .memory import MemoryView

__all__ = ["MemoryRetrieveParams"]


class MemoryRetrieveParams(TypedDict, total=False):
    view: MemoryView
