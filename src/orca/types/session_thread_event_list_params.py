from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SessionThreadEventListParams"]


class SessionThreadEventListParams(TypedDict, total=False):
    limit: int

    page: str
