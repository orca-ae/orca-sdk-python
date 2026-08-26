from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .agent_shared import ModelEffort, McpServerDefinition, AgentMultiagentDefinition

__all__ = ["Agent", "AgentResponseModel", "AgentResponseSkillDefinition", "DeletedAgent"]


class AgentModelBasic(BaseModel):
    id: str

    speed: Optional[Literal["standard", "fast"]] = None

    effort: Optional[ModelEffort] = None


class AgentModelProviderQualified(BaseModel):
    id: str

    provider: str


AgentResponseModel: TypeAlias = Union[AgentModelBasic, AgentModelProviderQualified]


class AgentResponseSkillDefinition(BaseModel):
    type: str
    """Skill source discriminator; see `AgentSkillDefinitionParam.type`."""

    skill_id: str

    version: str


class AgentToolDefinition(BaseModel):
    """A tool entry on an agent.

    Left open rather than modelled as a closed union: the contract renders these
    inline with per-variant extras, and `BaseModel` preserves unknown fields, so a
    tool type added server-side still round-trips.
    """

    type: str


class Agent(BaseModel):
    id: str

    type: Literal["agent"]

    name: str

    description: Optional[str] = None

    model: AgentResponseModel

    system: Optional[str] = None

    mcp_servers: List[McpServerDefinition]

    tools: List[AgentToolDefinition]

    skills: List[AgentResponseSkillDefinition]

    multiagent: Optional[AgentMultiagentDefinition] = None

    metadata: Dict[str, str]

    version: int

    created_at: str

    updated_at: str

    archived_at: Optional[str] = None
    """Present but null while the agent is active."""


class DeletedAgent(BaseModel):
    id: str

    type: Literal["agent_deleted"]
