from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Required, TypedDict

from .guardrail_shared import GuardrailPhase, GuardrailScope, GuardrailRuleParam

__all__ = ["GuardrailCreateParams"]


class GuardrailCreateParams(TypedDict, total=False):
    name: Required[str]

    rule: Required[GuardrailRuleParam]

    description: Optional[str]

    enabled: bool

    phases: List[GuardrailPhase]

    scope: GuardrailScope

    metadata: Dict[str, str]
