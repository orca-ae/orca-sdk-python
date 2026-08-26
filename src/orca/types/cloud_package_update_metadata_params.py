from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["CloudPackageUpdateMetadataParams"]


class CloudPackageUpdateMetadataParams(TypedDict, total=False):
    description: str

    contact: str

    createTime: int
    """Epoch milliseconds, per the contract's int64 timestamps."""

    modificationTime: int
    """Epoch milliseconds, per the contract's int64 timestamps."""

    properties: Dict[str, str]
