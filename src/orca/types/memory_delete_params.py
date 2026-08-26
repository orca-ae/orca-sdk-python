from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["MemoryDeleteParams"]


class MemoryDeleteParams(TypedDict, total=False):
    expected_content_sha256: str
    """Guard the delete: it is rejected unless the memory's content still hashes to
    this value."""
