from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SessionThreadListParams"]


class SessionThreadListParams(TypedDict, total=False):
    limit: int

    page: str
