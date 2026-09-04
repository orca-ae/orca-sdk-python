from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["GuardrailListParams"]


class GuardrailListParams(TypedDict, total=False):
    limit: int

    page: str

    include_archived: bool
