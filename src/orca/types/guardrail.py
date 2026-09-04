from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .guardrail_shared import GuardrailPhase, GuardrailScope, GuardrailVerdict

__all__ = [
    "Guardrail",
    "DeletedGuardrail",
    "GuardrailRule",
    "GuardrailBuiltinRule",
    "GuardrailExpressionRule",
]


class GuardrailBuiltinRule(BaseModel):
    kind: Literal["builtin"]

    builtin: str

    params: Optional[Dict[str, object]] = None


class GuardrailExpressionRule(BaseModel):
    kind: Literal["expression"]

    expression: str

    on_false: GuardrailVerdict

    reason: Optional[str] = None


GuardrailRule: TypeAlias = Union[GuardrailBuiltinRule, GuardrailExpressionRule]


class Guardrail(BaseModel):
    id: str

    type: Literal["guardrail"]

    name: str

    description: str

    enabled: bool

    phases: List[GuardrailPhase]

    scope: GuardrailScope

    rule: GuardrailRule

    metadata: Optional[Dict[str, str]] = None

    archived_at: Optional[str] = None

    created_at: str

    updated_at: str


class DeletedGuardrail(BaseModel):
    id: str

    type: Literal["guardrail_deleted"]
