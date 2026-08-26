from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

from .agent_shared import AgentMcpServerParam, AgentToolDefinitionParam

__all__ = ["SessionUpdateParams", "SessionAgentUpdateParam"]


class SessionAgentUpdateParam(TypedDict, total=False):
    """Narrow edits to the session's frozen agent snapshot."""

    tools: List[AgentToolDefinitionParam]

    mcp_servers: List[AgentMcpServerParam]


class SessionUpdateParams(TypedDict, total=False):
    agent: SessionAgentUpdateParam

    vault_ids: List[str]

    title: Optional[str]

    metadata: Optional[Dict[str, Optional[str]]]
    """A null value removes that individual key."""
