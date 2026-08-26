from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SessionFileListParams"]


class SessionFileListParams(TypedDict, total=False):
    limit: int

    after_id: str
    """Page forward from this file id."""

    before_id: str
    """Page backward from this file id. Never combine with `after_id`."""
