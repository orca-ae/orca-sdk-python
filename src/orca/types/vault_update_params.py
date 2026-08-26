from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["VaultUpdateParams"]


class VaultUpdateParams(TypedDict, total=False):
    display_name: Optional[str]

    metadata: Optional[Dict[str, Optional[str]]]
    """A null value removes that individual key."""
