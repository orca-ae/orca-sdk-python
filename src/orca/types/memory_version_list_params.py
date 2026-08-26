from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .memory import MemoryView
from .._utils import PropertyInfo
from .memory_version import MemoryVersionOperation

__all__ = ["MemoryVersionListParams"]


class MemoryVersionListParams(TypedDict, total=False):
    limit: int

    page: str
    """Opaque page token from a previous response's `next_page`."""

    memory_id: str

    api_key_id: str

    operation: MemoryVersionOperation

    created_at_gte: Annotated[str, PropertyInfo(alias="created_at[gte]")]

    created_at_lte: Annotated[str, PropertyInfo(alias="created_at[lte]")]

    view: MemoryView
