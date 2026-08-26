from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["FileUploadParams"]


class FileUploadParams(TypedDict, total=False):
    file: Required[FileTypes]
    """The file bytes to upload.

    Pass a `(filename, content, content_type)` tuple to control the MIME type the
    server records; a bare path or file object leaves that inference to httpx.
    """
