# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Dict, List, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "GuardrailPhase",
    "GuardrailScope",
    "GuardrailVerdict",
    "GuardrailStateScope",
    "GuardrailRuleParam",
    "GuardrailBuiltinRuleParam",
    "GuardrailExpressionRuleParam",
    "GuardrailMode",
    "GuardrailDogwoodRuleParam",
    "GuardrailMCPManifestParam",
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
GuardrailStateScope: TypeAlias = Literal["turn", "session", "subject_window", "workspace_window"]
GuardrailMode: TypeAlias = Literal["enforce", "observe"]


class GuardrailBuiltinRuleParam(TypedDict, total=False):
    kind: Required[Literal["builtin"]]

    builtin: Required[str]

    params: Dict[str, object]


class GuardrailExpressionRuleParam(TypedDict, total=False):
    kind: Required[Literal["expression"]]

    expression: Required[str]

    on_false: Required[GuardrailVerdict]

    reason: str


class GuardrailMCPManifestParam(TypedDict, total=False):
    server: Required[str]
    url: Required[str]
    tools: Required[List[Dict[str, object]]]


class GuardrailDogwoodRuleParam(TypedDict, total=False):
    kind: Required[Literal["dogwood"]]
    policy: Required[str]
    applies_to: Literal["all_tools", "mcp_tools"]
    history: Literal["session", "principal"]
    mcp_manifests: List[GuardrailMCPManifestParam]


GuardrailRuleParam: TypeAlias = Union[
    GuardrailBuiltinRuleParam, GuardrailExpressionRuleParam, GuardrailDogwoodRuleParam
]
