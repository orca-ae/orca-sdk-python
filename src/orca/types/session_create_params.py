from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .agent_shared import (
    ModelConfigParam,
    AgentMcpServerParam,
    AgentToolDefinitionParam,
    AgentSkillDefinitionParam,
)
from .session_event import OutcomeRubricParam, MessageContentBlockParam
from .session_resource import SessionResourceRequestParam

__all__ = [
    "SessionCreateParams",
    "SessionAgentReferenceParam",
    "SessionAgentWithOverridesParam",
    "SessionAgentInputParam",
    "SessionUserMessageInitialEventParam",
    "SessionDefineOutcomeInitialEventParam",
    "SessionInitialEventParam",
]


class SessionAgentReferenceParam(TypedDict, total=False):
    type: Required[Literal["agent"]]

    id: Required[str]

    version: int
    """Pin the session to a historical agent version."""


class SessionAgentWithOverridesParam(TypedDict, total=False):
    type: Required[Literal["agent_with_overrides"]]

    id: Required[str]

    version: int

    model: Union[str, ModelConfigParam]

    system: Optional[str]

    tools: List[AgentToolDefinitionParam]

    mcp_servers: List[AgentMcpServerParam]

    skills: List[AgentSkillDefinitionParam]


SessionAgentInputParam: TypeAlias = Union[
    str,
    SessionAgentReferenceParam,
    SessionAgentWithOverridesParam,
]


class SessionUserMessageInitialEventParam(TypedDict, total=False):
    type: Required[Literal["user.message"]]

    content: Required[List[MessageContentBlockParam]]
    """Must hold at least one block; the server rejects an empty list."""


class SessionDefineOutcomeInitialEventParam(TypedDict, total=False):
    type: Required[Literal["user.define_outcome"]]

    description: Required[str]

    rubric: Required[OutcomeRubricParam]

    max_iterations: Optional[int]


SessionInitialEventParam: TypeAlias = Union[
    SessionUserMessageInitialEventParam,
    SessionDefineOutcomeInitialEventParam,
]


class SessionCreateParams(TypedDict, total=False):
    environment_id: Required[str]

    agent: SessionAgentInputParam
    """Agent reference. A plain string is shorthand for `{"id": <string>}`.

    Omit only when using the `agent_id` compatibility field instead.
    """

    agent_id: str
    """Compatibility form of the agent reference accepted by both backends."""

    vault_ids: List[str]

    title: Optional[str]

    metadata: Dict[str, str]

    resources: List[SessionResourceRequestParam]

    initial_events: List[SessionInitialEventParam]
    """Events applied before the agent's first turn."""
