from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["SessionListParams"]


class SessionListParams(TypedDict, total=False):
    agent_id: str
    """Filter to sessions owned by one agent."""

    limit: int

    page: str

    include_archived: Optional[bool]
