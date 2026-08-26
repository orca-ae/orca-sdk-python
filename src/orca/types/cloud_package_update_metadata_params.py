from __future__ import annotations

from typing import Dict
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CloudPackageUpdateMetadataParams"]


class CloudPackageUpdateMetadataParams(TypedDict, total=False):
    description: str

    contact: str

    create_time: Annotated[int, PropertyInfo(alias="createTime")]
    """Epoch milliseconds, per the contract's int64 timestamps. Sent as `createTime`."""

    modification_time: Annotated[int, PropertyInfo(alias="modificationTime")]
    """Epoch milliseconds, per the contract's int64 timestamps. Sent as `modificationTime`."""

    properties: Dict[str, str]
