from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._types import FileTypes
from .._utils import PropertyInfo
from .cloud_function_config import CloudFunctionConfigParam

__all__ = ["CloudFunctionCreateParams"]


class CloudFunctionCreateParams(TypedDict, total=False):
    data: FileTypes
    """The function archive itself. Mutually exclusive with `url` in practice."""

    url: str
    """A location the server fetches the archive from instead of `data`."""

    function_config: Annotated[CloudFunctionConfigParam, PropertyInfo(alias="functionConfig")]
    """Sent as `functionConfig`."""
