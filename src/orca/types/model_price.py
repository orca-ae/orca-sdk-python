from __future__ import annotations

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ModelPrice"]


class ModelPrice(BaseModel):
    type: Literal["model_price"]

    provider: str

    model_id: str

    input_per_million_tokens: float

    output_per_million_tokens: float

    cache_read_per_million_tokens: float

    cache_write_per_million_tokens: float
