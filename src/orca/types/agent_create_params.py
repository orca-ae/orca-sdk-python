from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Required, TypedDict

from .agent_shared import (
    ModelConfigParam,
    AgentMcpServerParam,
    AgentToolDefinitionParam,
    AgentSkillDefinitionParam,
    AgentMultiagentDefinitionParam,
)

__all__ = ["AgentCreateParams"]


class AgentCreateParams(TypedDict, total=False):
    model: Required[Union[str, ModelConfigParam]]
    """Model to use. A plain string is shorthand for `{"id": <string>}`."""

    name: Required[str]

    description: Optional[str]

    system: Optional[str]

    mcp_servers: List[AgentMcpServerParam]

    tools: List[AgentToolDefinitionParam]

    skills: List[AgentSkillDefinitionParam]

    guardrail_ids: List[str]
    """Guardrails explicitly attached to this agent. Requires `orca-beta`."""

    metadata: Dict[str, str]

    multiagent: Optional[AgentMultiagentDefinitionParam]
