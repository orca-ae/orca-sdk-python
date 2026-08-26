from __future__ import annotations

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CloudAPIResource", "CloudAPIResourceList"]


class CloudAPIResource(BaseModel):
    name: str
    """Path segment the resource is served under, e.g. `"connections"`."""

    namespaced: bool
    """Whether the resource is scoped to a namespace rather than the whole group."""

    kind: str
    """Schema kind the resource returns, e.g. `"Connection"`."""


class CloudAPIResourceList(BaseModel):
    kind: Literal["APIResourceList"]

    group_version: str
    """The `<group>/<version>` this listing describes, e.g. `"cloud.sn.io/v1"`.

    `GET /apis` answers *which* extension groups exist; this answers what a single
    group version actually serves.
    """

    resources: List[CloudAPIResource]
