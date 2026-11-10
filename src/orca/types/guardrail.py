# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Dict, List, Union, Optional, Annotated
from typing_extensions import Literal, TypeAlias

from pydantic import field_validator

from .._utils import PropertyInfo
from .._models import BaseModel
from .guardrail_shared import GuardrailMode, GuardrailPhase, GuardrailScope, GuardrailVerdict

__all__ = [
    "Guardrail",
    "DeletedGuardrail",
    "GuardrailRule",
    "GuardrailBuiltinRule",
    "GuardrailExpressionRule",
    "GuardrailDogwoodRule",
    "GuardrailMCPManifest",
    "GuardrailUnknownRule",
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


class GuardrailMCPManifest(BaseModel):
    server: str
    url: str
    tools: List[Dict[str, object]]


class GuardrailDogwoodRule(BaseModel):
    kind: Literal["dogwood"]
    policy: str
    applies_to: Optional[Literal["all_tools", "mcp_tools"]] = None
    history: Optional[Literal["session", "principal"]] = None
    mcp_manifests: Optional[List[GuardrailMCPManifest]] = None


class GuardrailUnknownRule(BaseModel):
    """GuardrailUnknownRule preserves future rule kinds without accepting malformed known rules."""

    kind: str

    @field_validator("kind")
    @classmethod
    def _reject_known_kind(cls, value: str) -> str:
        if value in {"builtin", "expression", "dogwood"}:
            raise ValueError("Known rule kinds must match their declared schema")
        return value


GuardrailRule: TypeAlias = Annotated[
    Union[GuardrailBuiltinRule, GuardrailExpressionRule, GuardrailDogwoodRule, GuardrailUnknownRule],
    PropertyInfo(discriminator="kind"),
]


class Guardrail(BaseModel):
    id: str

    type: Literal["guardrail"]

    name: str

    description: str

    enabled: bool

    mode: Optional[GuardrailMode] = None

    warnings: Optional[List[str]] = None

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
