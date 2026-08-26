from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["TriggerListParams"]


class TriggerListParams(TypedDict, total=False):
    limit: int

    page: str
    """Opaque page token from a previous response's `next_page`."""

    agent_id: str
