# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field

from .._models import BaseModel
from .guardrail_shared import GuardrailMode, GuardrailStateScope

__all__ = ["GuardrailBundle", "GuardrailBundleScope", "EffectiveGuardrail"]


class GuardrailBundleScope(BaseModel):
    org_id: str
    workspace_id: str


class EffectiveGuardrail(BaseModel):
    id: str
    name: str
    tier: Literal["session", "agent", "workspace", "organization"]
    phases: List[str]
    # The effective bundle deliberately leaves evaluated rule shapes open.
    rule: Optional[object] = None
    stateful: bool
    mode: GuardrailMode
    state_scope: Optional[GuardrailStateScope] = None
    subagent_id: Optional[str] = None


class GuardrailBundle(BaseModel):
    schema_: Literal["1"] = Field(alias="schema")
    bundle_id: str
    generation: int
    scope: GuardrailBundleScope
    runtime_config_revision: str
    issued_at: str
    expires_at: str
    seed_verdict: Literal["allow"]
    guardrails: List[EffectiveGuardrail]
    omitted_rules: int
