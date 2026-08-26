from __future__ import annotations

from typing_extensions import TypedDict

from .memory import MemoryView

__all__ = ["MemoryVersionRetrieveParams"]


class MemoryVersionRetrieveParams(TypedDict, total=False):
    view: MemoryView
