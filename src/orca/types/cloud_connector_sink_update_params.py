from __future__ import annotations

from typing_extensions import TypedDict

from .._types import FileTypes
from .cloud_connector_sink import CloudSinkConfigParam
from .cloud_connector_shared import CloudRuntimeUpdateOptionsParam

__all__ = ["CloudSinkUpdateParams"]


class CloudSinkUpdateParams(TypedDict, total=False):
    """Body of a sink update, sent as `multipart/form-data`.

    The update is a full replacement (`PUT`), so send the complete `sinkConfig`
    rather than only the fields that changed.
    """

    data: FileTypes
    """The connector package bytes, when uploading rather than referencing a URL."""

    url: str
    """Location the server fetches the connector package from."""

    sinkConfig: CloudSinkConfigParam

    updateOptions: CloudRuntimeUpdateOptionsParam
