from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ModelPriceRetrieveParams"]


class ModelPriceRetrieveParams(TypedDict, total=False):
    provider: str
