from __future__ import annotations

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["APIGroupVersion", "APIGroup", "APIGroupList"]


class APIGroupVersion(BaseModel):
    group_version: str
    """`<group>/<version>`, the prefix under `/apis` that serves this group version."""

    version: str
    """The version alone, e.g. `v1`."""


class APIGroup(BaseModel):
    name: str
    """Extension group name, e.g. `"cloud.sn.io"`."""

    versions: List[APIGroupVersion]

    preferred_version: APIGroupVersion


class APIGroupList(BaseModel):
    kind: Literal["APIGroupList"]

    groups: List[APIGroup]
    """Extension API groups this deployment serves beyond the core surface.

    An empty list means "no extensions installed" — a normal deployment shape, not
    an error. That is distinct from the 404 an older, pre-discovery deployment
    returns for the same call.
    """
