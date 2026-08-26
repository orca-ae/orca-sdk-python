from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._types import FileTypes
from .._utils import PropertyInfo
from .cloud_function_config import CloudFunctionConfigParam
from .cloud_function_shared import CloudRuntimeUpdateOptionsParam

__all__ = ["CloudFunctionUpdateParams"]


class CloudFunctionUpdateParams(TypedDict, total=False):
    data: FileTypes
    """A replacement function archive. Mutually exclusive with `url` in practice."""

    url: str
    """A location the server fetches the replacement archive from instead of `data`."""

    function_config: Annotated[CloudFunctionConfigParam, PropertyInfo(alias="functionConfig")]
    """Sent as `functionConfig`."""

    update_options: Annotated[CloudRuntimeUpdateOptionsParam, PropertyInfo(alias="updateOptions")]
    """Sent as `updateOptions`."""
