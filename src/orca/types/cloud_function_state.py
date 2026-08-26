"""Function state entries.

Wire names are mirrored verbatim; see `cloud_function_shared` for why.
"""

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .._models import BaseModel

__all__ = ["CloudFunctionState", "CloudFunctionStateParam"]


class CloudFunctionState(BaseModel):
    key: Optional[str] = None

    stringValue: Optional[str] = None

    byteValue: Optional[str] = None
    """Base64 text: the contract declares this as a byte-formatted string."""

    numberValue: Optional[int] = None

    version: Optional[int] = None


class CloudFunctionStateParam(TypedDict, total=False):
    key: str

    stringValue: str

    byteValue: str
    """Base64 text: the contract declares this as a byte-formatted string."""

    numberValue: int

    version: int
