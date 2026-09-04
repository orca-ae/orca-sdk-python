from __future__ import annotations

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["APIResource", "APIResourceList"]


class APIResource(BaseModel):
    name: str

    namespaced: bool

    kind: str


class APIResourceList(BaseModel):
    kind: Literal["APIResourceList"]

    group_version: str

    resources: List[APIResource]
