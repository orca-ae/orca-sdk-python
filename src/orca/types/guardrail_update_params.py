from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

from .guardrail_shared import GuardrailPhase, GuardrailScope, GuardrailRuleParam

__all__ = ["GuardrailUpdateParams"]


class GuardrailUpdateParams(TypedDict, total=False):
    name: str

    description: Optional[str]

    enabled: bool

    phases: List[GuardrailPhase]

    scope: GuardrailScope

    rule: GuardrailRuleParam

    metadata: Dict[str, Optional[str]]
