"""Pin the optional policy fields shared by the core spec and public SDK types."""

from __future__ import annotations

import re
import inspect
from typing import List, Optional, get_type_hints
from pathlib import Path

from orca import omit
from orca.types import Agent
from orca.resources.agents import Agents, AsyncAgents
from orca.types.agent_create_params import AgentCreateParams
from orca.types.agent_update_params import AgentUpdateParams
from orca.types.session_create_params import SessionAgentReferenceParam, SessionAgentWithOverridesParam


def test_core_spec_declares_all_guardrail_fields() -> None:
    spec = (Path(__file__).parents[1] / "openapi" / "managed-agents.yaml").read_text()
    # Read only this inline property, stopping when indentation returns to its level.
    fields = list(re.finditer(r"(?m)^(?P<indent> +)guardrail_ids:\n(?P<body>(?:(?P=indent) +[^\n]*\n)+)", spec))
    assert len(fields) == 9  # Three inputs and six Agent response appearances.
    bodies = [match["body"] for match in fields]
    assert all("type: array" in body and "type: string" in body for body in bodies)
    assert all("pattern: ^(?:grd)_[A-Za-z0-9_-]+$" in body for body in bodies)
    assert sum("maxItems: 64" in body for body in bodies) == 3
    assert sum("default: []" in body for body in bodies) == 1
    assert sum("nullable: true" in body for body in bodies) == 1


def test_guardrail_public_types_and_signatures() -> None:
    assert get_type_hints(AgentCreateParams)["guardrail_ids"] == List[str]
    assert get_type_hints(AgentUpdateParams)["guardrail_ids"] == Optional[List[str]]
    assert get_type_hints(SessionAgentWithOverridesParam)["guardrail_ids"] == List[str]
    assert "guardrail_ids" not in get_type_hints(SessionAgentReferenceParam)
    assert Agent.model_fields["guardrail_ids"].annotation == Optional[List[str]]
    for sync, async_ in ((Agents.create, AsyncAgents.create), (Agents.update, AsyncAgents.update)):
        assert inspect.signature(sync) == inspect.signature(async_)
        assert inspect.signature(sync).parameters["guardrail_ids"].default is omit
