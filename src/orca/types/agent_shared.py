from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._models import BaseModel

__all__ = [
    "ModelEffortType",
    "ModelEffort",
    "ModelConfigParam",
    "McpServerDefinition",
    "AgentMcpServerParam",
    "AgentCustomToolInputSchemaParam",
    "AgentPermissionPolicyParam",
    "AgentToolDefaultConfigParam",
    "AgentNamedToolConfigParam",
    "AgentToolConfigsParam",
    "AgentToolDefinitionParam",
    "AgentSkillDefinitionParam",
    "AgentMultiagentRosterEntryParam",
    "AgentMultiagentDefinitionParam",
    "AgentMultiagentDefinition",
]

ModelEffortType: TypeAlias = Literal["low", "medium", "high", "xhigh", "max"]


class ModelEffort(BaseModel):
    type: ModelEffortType


class ModelEffortParam(TypedDict, total=False):
    type: Required[ModelEffortType]


class ModelConfigParam(TypedDict, total=False):
    id: Required[str]

    provider: str
    """Deployment or provider identifier when the model is provider-qualified."""

    speed: Optional[Literal["standard", "fast"]]

    effort: Union[ModelEffortType, ModelEffortParam, None]


class McpServerDefinition(BaseModel):
    name: str

    type: Literal["url"]

    url: str


class AgentMcpServerParam(TypedDict, total=False):
    name: Required[str]

    url: Required[str]

    type: Literal["url"]
    """Optional on input; the server infers `"url"` when omitted."""


class AgentCustomToolInputSchemaParam(TypedDict, total=False):
    type: Required[Literal["object"]]

    properties: Optional[Dict[str, object]]

    required: Optional[List[str]]


class AgentPermissionPolicyParam(TypedDict, total=False):
    type: Required[Literal["always_allow", "always_ask"]]


class AgentToolDefaultConfigParam(TypedDict, total=False):
    enabled: Optional[bool]

    permission_policy: Optional[AgentPermissionPolicyParam]


class AgentNamedToolConfigParam(AgentToolDefaultConfigParam, total=False):
    name: Required[str]


AgentToolConfigsParam: TypeAlias = Union[
    List[AgentNamedToolConfigParam],
    Dict[str, AgentToolDefaultConfigParam],
]


class AgentBuiltinToolsetDefinitionParam(TypedDict, total=False):
    type: Required[Literal["agent_toolset", "agent_toolset_20260401"]]

    configs: AgentToolConfigsParam

    default_config: Optional[AgentToolDefaultConfigParam]


class AgentMcpToolsetDefinitionParam(TypedDict, total=False):
    type: Required[Literal["mcp_toolset"]]

    mcp_server_name: Required[str]

    configs: AgentToolConfigsParam

    default_config: Optional[AgentToolDefaultConfigParam]


class AgentCustomToolDefinitionParam(TypedDict, total=False):
    type: Required[Literal["custom"]]

    name: Required[str]

    description: Required[str]

    input_schema: Required[AgentCustomToolInputSchemaParam]


AgentToolDefinitionParam: TypeAlias = Union[
    AgentBuiltinToolsetDefinitionParam,
    AgentMcpToolsetDefinitionParam,
    AgentCustomToolDefinitionParam,
]


class AgentSkillDefinitionParam(TypedDict, total=False):
    type: Required[str]
    """Skill source discriminator.

    Typed as an open string rather than a closed set: the accepted values are defined
    by the API contract (see `openapi/managed-agents.yaml`), the server validates them,
    and new sources can appear without an SDK release. The TypeScript client models
    this shape as open for the same reason.
    """

    skill_id: Required[str]

    version: Optional[str]


class AgentRosterAgentParam(TypedDict, total=False):
    type: Required[Literal["agent"]]

    id: Required[str]

    version: int


class AgentRosterSelfParam(TypedDict, total=False):
    type: Required[Literal["self"]]


AgentMultiagentRosterEntryParam: TypeAlias = Union[str, AgentRosterAgentParam, AgentRosterSelfParam]


class AgentMultiagentDefinitionParam(TypedDict, total=False):
    type: Required[Literal["coordinator"]]

    agents: Required[List[AgentMultiagentRosterEntryParam]]


class AgentMultiagentDefinition(BaseModel):
    type: Literal["coordinator"]

    agents: List[object]
    """Roster entries: an agent id, an `{"type": "agent"}` reference, or `{"type": "self"}`."""
