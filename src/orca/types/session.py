from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, TypeAlias

from .agent import AgentResponseModel, AgentToolDefinition
from .._models import BaseModel
from .agent_shared import SkillSource, McpServerDefinition
from .session_resource import SessionResource

__all__ = [
    "SessionStats",
    "SessionCacheCreationUsage",
    "SessionUsage",
    "SessionStatus",
    "SessionTiming",
    "OutcomeEvaluation",
    "SessionAgentSkillDefinition",
    "SessionAgentMember",
    "SessionAgentMultiagentDefinition",
    "SessionAgent",
    "Session",
    "DeletedSession",
]


class SessionStats(BaseModel):
    active_seconds: Optional[int] = None

    duration_seconds: Optional[int] = None


class SessionCacheCreationUsage(BaseModel):
    ephemeral_1h_input_tokens: Optional[int] = None

    ephemeral_5m_input_tokens: Optional[int] = None


class SessionUsage(BaseModel):
    input_tokens: Optional[int] = None

    output_tokens: Optional[int] = None

    cache_read_input_tokens: Optional[int] = None

    cache_creation: Optional[SessionCacheCreationUsage] = None


SessionStatus: TypeAlias = Literal["rescheduling", "running", "idle", "terminated"]


class SessionTiming(BaseModel):
    started_at: Optional[str] = None
    """Null until the session first runs."""

    last_active_at: Optional[str] = None

    active_seconds: int

    duration_seconds: int


class OutcomeEvaluation(BaseModel):
    """One evaluation of a `user.define_outcome` goal.

    Carries extra fields for evaluator-specific detail, which `BaseModel` preserves.
    """

    type: Literal["outcome_evaluation"]

    outcome_id: str

    description: str

    result: str

    explanation: Optional[str] = None

    iteration: int

    completed_at: Optional[str] = None


class SessionAgentSkillDefinition(BaseModel):
    type: SkillSource
    """Where the skill comes from. Values are fixed by the API contract."""

    skill_id: str

    version: Optional[str] = None
    """Optional on a snapshot, unlike the required version on a live agent."""


class SessionAgentMember(BaseModel):
    """An agent snapshot frozen into the session at creation time.

    The session keeps its own copy so later edits to the agent do not retroactively
    change a running or finished session.
    """

    id: str

    type: Literal["agent"]

    name: str

    description: Optional[str] = None

    version: int

    model: AgentResponseModel

    system: Optional[str] = None

    tools: List[AgentToolDefinition]

    mcp_servers: List[McpServerDefinition]

    skills: List[SessionAgentSkillDefinition]


class SessionAgentMultiagentDefinition(BaseModel):
    type: Literal["coordinator"]

    agents: List[SessionAgentMember]


class SessionAgent(SessionAgentMember):
    multiagent: Optional[SessionAgentMultiagentDefinition] = None


class Session(BaseModel):
    id: str

    type: Literal["session"]

    agent: SessionAgent
    """Agent snapshot taken when the session was created."""

    environment_id: str

    vault_ids: List[str]

    status: SessionStatus

    title: Optional[str] = None

    stats: SessionStats

    timing: Optional[SessionTiming] = None

    deployment_id: Optional[str] = None

    outcome_evaluations: List[OutcomeEvaluation]

    usage: SessionUsage

    resources: List[SessionResource]

    metadata: Dict[str, str]

    created_at: str

    updated_at: str

    archived_at: Optional[str] = None
    """Present but null while the session is active."""


class DeletedSession(BaseModel):
    id: str

    type: Literal["session_deleted"]
