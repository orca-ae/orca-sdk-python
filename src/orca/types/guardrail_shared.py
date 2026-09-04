from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "GuardrailPhase",
    "GuardrailScope",
    "GuardrailVerdict",
    "GuardrailStateScope",
    "GuardrailRuleParam",
    "GuardrailBuiltinRuleParam",
    "GuardrailExpressionRuleParam",
]

GuardrailPhase: TypeAlias = Literal[
    "request",
    "tool_call",
    "tool_result",
    "response",
    "llm_request",
    "llm_response",
]
GuardrailScope: TypeAlias = Literal["organization", "workspace", "explicit"]
GuardrailVerdict: TypeAlias = Literal["ask", "deny"]
GuardrailStateScope: TypeAlias = Literal["turn", "session", "subject_window"]


class GuardrailBuiltinRuleParam(TypedDict, total=False):
    kind: Required[Literal["builtin"]]

    builtin: Required[str]

    params: Dict[str, object]


class GuardrailExpressionRuleParam(TypedDict, total=False):
    kind: Required[Literal["expression"]]

    expression: Required[str]

    on_false: Required[GuardrailVerdict]

    reason: str


GuardrailRuleParam: TypeAlias = Union[GuardrailBuiltinRuleParam, GuardrailExpressionRuleParam]
