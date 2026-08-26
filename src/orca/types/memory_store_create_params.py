from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["MemoryStoreCreateParams"]


class MemoryStoreCreateParams(TypedDict, total=False):
    name: Required[str]
    """Human-readable name; 1-255 characters."""

    description: str
    """Free-text description, up to 1024 characters."""

    metadata: Dict[str, str]
    """Arbitrary string key/value pairs."""
