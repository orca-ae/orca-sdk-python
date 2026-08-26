from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["FileListParams"]


class FileListParams(TypedDict, total=False):
    limit: int

    after_id: str
    """Return files after this id. Never combine with `before_id`."""

    before_id: str
    """Return files before this id. Never combine with `after_id`."""
