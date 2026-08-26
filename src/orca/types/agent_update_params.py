from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import TypedDict

from .agent_shared import (
    ModelConfigParam,
    AgentMcpServerParam,
    AgentToolDefinitionParam,
    AgentSkillDefinitionParam,
    AgentMultiagentDefinitionParam,
)

__all__ = ["AgentUpdateParams"]


class AgentUpdateParams(TypedDict, total=False):
    version: int
    """When provided, must match the agent's current version.

    This is the optimistic-concurrency check: a mismatch means someone else updated
    the agent since you read it, and the server rejects the write rather than
    silently clobbering their change.
    """

    name: str

    description: Optional[str]

    model: Union[str, ModelConfigParam]

    system: Optional[str]

    mcp_servers: Optional[List[AgentMcpServerParam]]

    tools: Optional[List[AgentToolDefinitionParam]]

    skills: Optional[List[AgentSkillDefinitionParam]]

    multiagent: Optional[AgentMultiagentDefinitionParam]

    metadata: Optional[Dict[str, Optional[str]]]
    """A null value removes that individual key."""
