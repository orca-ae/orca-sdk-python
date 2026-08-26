from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SessionEventListParams"]


class SessionEventListParams(TypedDict, total=False):
    limit: int

    page: str

    created_at_gt: Annotated[str, PropertyInfo(alias="created_at[gt]")]

    created_at_gte: Annotated[str, PropertyInfo(alias="created_at[gte]")]

    created_at_lt: Annotated[str, PropertyInfo(alias="created_at[lt]")]

    created_at_lte: Annotated[str, PropertyInfo(alias="created_at[lte]")]

    order: Literal["asc", "desc"]

    types: Union[str, List[str]]

    subpath: str
