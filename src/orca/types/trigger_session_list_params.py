from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["TriggerSessionListParams"]


class TriggerSessionListParams(TypedDict, total=False):
    limit: int

    page: str
    """Opaque page token from a previous response's `next_page`."""

    include_archived: Optional[bool]
