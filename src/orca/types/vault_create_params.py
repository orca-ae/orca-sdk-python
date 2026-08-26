from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["VaultCreateParams"]


class VaultCreateParams(TypedDict, total=False):
    display_name: Required[str]

    metadata: Dict[str, str]
    """Arbitrary string key/value pairs."""
