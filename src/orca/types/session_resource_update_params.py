from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SessionResourceUpdateParams"]


class SessionResourceUpdateParams(TypedDict, total=False):
    authorization_token: Required[str]
    """Replacement token for a repository resource. Write-only; never returned."""
