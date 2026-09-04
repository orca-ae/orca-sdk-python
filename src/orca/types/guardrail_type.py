from __future__ import annotations

from typing import Dict, List, Optional

import pydantic

from .._models import BaseModel
from .guardrail_shared import GuardrailPhase, GuardrailVerdict, GuardrailStateScope

__all__ = ["GuardrailType", "GuardrailTypeList"]


class GuardrailType(BaseModel):
    name: str

    title: str

    description: str

    phases: List[GuardrailPhase]

    stateful: bool

    state_scope: Optional[GuardrailStateScope] = pydantic.Field(default=None, alias="stateScope")

    verdicts: List[GuardrailVerdict]

    params_schema: Dict[str, object] = pydantic.Field(alias="paramsSchema")
    """JSON Schema for the builtin's parameter object."""


class GuardrailTypeList(BaseModel):
    data: List[GuardrailType]
