from __future__ import annotations

from typing_extensions import TypedDict

from .cloud_connection_shared import CloudConnectionSpecParam, CloudConnectionStatusParam

__all__ = ["CloudConnectionValidateParams"]


class CloudConnectionValidateParams(TypedDict, total=False):
    name: str

    spec: CloudConnectionSpecParam

    status: CloudConnectionStatusParam

    internal: bool

    clusterRef: str
