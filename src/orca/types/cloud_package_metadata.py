"""Package metadata.

Wire names are mirrored verbatim; the cloud extension serves camelCase JSON and
`AGENTS.md` §5 says we mirror the wire shape rather than re-spell it.
"""

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .._models import BaseModel

__all__ = ["CloudPackageMetadata", "CloudPackageMetadataParam"]


class CloudPackageMetadata(BaseModel):
    description: Optional[str] = None

    contact: Optional[str] = None

    createTime: Optional[int] = None
    """Epoch milliseconds, per the contract's int64 timestamps."""

    modificationTime: Optional[int] = None
    """Epoch milliseconds, per the contract's int64 timestamps."""

    properties: Optional[Dict[str, str]] = None


class CloudPackageMetadataParam(TypedDict, total=False):
    description: str

    contact: str

    createTime: int
    """Epoch milliseconds, per the contract's int64 timestamps."""

    modificationTime: int
    """Epoch milliseconds, per the contract's int64 timestamps."""

    properties: Dict[str, str]
