from __future__ import annotations

from typing_extensions import TypedDict

from .._types import FileTypes
from .cloud_connector_shared import CloudRuntimeUpdateOptionsParam
from .cloud_connector_source import CloudSourceConfigParam

__all__ = ["CloudSourceUpdateParams"]


class CloudSourceUpdateParams(TypedDict, total=False):
    """Body of a source update, sent as `multipart/form-data`.

    The update is a full replacement (`PUT`), so send the complete `sourceConfig`
    rather than only the fields that changed.
    """

    data: FileTypes
    """The connector package bytes, when uploading rather than referencing a URL."""

    url: str
    """Location the server fetches the connector package from."""

    sourceConfig: CloudSourceConfigParam

    updateOptions: CloudRuntimeUpdateOptionsParam
