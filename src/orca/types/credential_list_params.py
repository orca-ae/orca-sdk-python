from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CredentialListParams"]


class CredentialListParams(TypedDict, total=False):
    limit: int

    page: str
    """Opaque page token from a previous response's `next_page`."""

    include_archived: bool
    """Include archived credentials in the results."""
