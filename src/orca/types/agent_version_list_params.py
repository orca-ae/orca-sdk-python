from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AgentVersionListParams"]


class AgentVersionListParams(TypedDict, total=False):
    limit: int

    page: str
    """Opaque page token from a previous response's `next_page`."""
