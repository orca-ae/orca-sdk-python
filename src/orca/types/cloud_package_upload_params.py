from __future__ import annotations

from typing_extensions import TypedDict

from .._types import FileTypes
from .cloud_package_metadata import CloudPackageMetadataParam

__all__ = ["CloudPackageUploadParams"]


class CloudPackageUploadParams(TypedDict, total=False):
    metadata: CloudPackageMetadataParam

    file: FileTypes
    """The package bytes."""
