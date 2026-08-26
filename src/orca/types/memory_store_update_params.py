from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["MemoryStoreUpdateParams"]


class MemoryStoreUpdateParams(TypedDict, total=False):
    name: Optional[str]

    description: Optional[str]

    metadata: Optional[Dict[str, Optional[str]]]
    """Metadata patch. A null value removes that individual key; omit to preserve."""
