from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .cloud_connection_shared import CloudConnectionSpecParam, CloudConnectionStatusParam

__all__ = ["CloudConnectionUpdateParams"]


class CloudConnectionUpdateParams(TypedDict, total=False):
    name: str

    spec: CloudConnectionSpecParam

    status: CloudConnectionStatusParam

    internal: bool

    cluster_ref: Annotated[str, PropertyInfo(alias="clusterRef")]
    """Sent as `clusterRef`."""
