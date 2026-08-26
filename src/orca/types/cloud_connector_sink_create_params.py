from __future__ import annotations

from typing_extensions import TypedDict

from .._types import FileTypes
from .cloud_connector_sink import CloudSinkConfigParam

__all__ = ["CloudSinkCreateParams"]


class CloudSinkCreateParams(TypedDict, total=False):
    """Body of a sink registration, sent as `multipart/form-data`.

    Supply the connector package either inline as `data` or by reference as `url`;
    `sinkConfig` travels as its own JSON part rather than as form fields.
    """

    data: FileTypes
    """The connector package bytes, when uploading rather than referencing a URL."""

    url: str
    """Location the server fetches the connector package from."""

    sinkConfig: CloudSinkConfigParam
