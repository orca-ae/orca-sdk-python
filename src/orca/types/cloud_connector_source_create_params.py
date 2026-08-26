from __future__ import annotations

from typing_extensions import TypedDict

from .._types import FileTypes
from .cloud_connector_source import CloudSourceConfigParam

__all__ = ["CloudSourceCreateParams"]


class CloudSourceCreateParams(TypedDict, total=False):
    """Body of a source registration, sent as `multipart/form-data`.

    Supply the connector package either inline as `data` or by reference as `url`;
    `sourceConfig` travels as its own JSON part rather than as form fields.
    """

    data: FileTypes
    """The connector package bytes, when uploading rather than referencing a URL."""

    url: str
    """Location the server fetches the connector package from."""

    sourceConfig: CloudSourceConfigParam
