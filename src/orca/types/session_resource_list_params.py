from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SessionResourceListParams"]


class SessionResourceListParams(TypedDict, total=False):
    limit: int

    page: str
