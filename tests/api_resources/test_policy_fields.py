from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

AGENT: dict[str, Any] = {
    "id": "agent_123",
    "type": "agent",
    "name": "demo",
    "description": None,
    "model": {"id": "some-model"},
    "system": None,
    "mcp_servers": [],
    "tools": [],
    "skills": [],
    "guardrail_ids": ["grd_example"],
    "multiagent": None,
    "metadata": {},
    "version": 1,
    "created_at": "2026-09-01T00:00:00Z",
    "updated_at": "2026-09-01T00:00:00Z",
    "archived_at": None,
}

SESSION: dict[str, Any] = {
    "id": "session_123",
    "type": "session",
    "agent": {**AGENT, "skills": [], "guardrail_ids": ["grd_example"]},
    "environment_id": "env_123",
    "vault_ids": [],
    "status": "running",
    "title": None,
    "stats": {},
    "outcome_evaluations": [],
    "usage": {},
    "resources": [],
    "metadata": {},
    "created_at": "2026-09-01T00:00:00Z",
    "updated_at": "2026-09-01T00:00:00Z",
    "archived_at": None,
}


def _req(route: Any) -> httpx2.Request:
    return cast("httpx2.Request", route.calls[0].request)


def _gate(respx_mock: MockRouter, client: Orca | AsyncOrca, *, available: bool = True) -> Any:
    client._extension_groups.clear()
    groups = [{"name": "policy.runorca.ai"}] if available else []
    return respx_mock.get("/apis").mock(
        return_value=httpx2.Response(200, json={"kind": "APIGroupList", "groups": groups})
    )


class TestPolicyFields:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_agent_create_gates_and_sends_guardrail_ids(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        agent = client.agents.create(
            model="some-model",
            name="demo",
            guardrail_ids=["grd_example"],
            extra_headers={"orca-beta": "guardrails-2025-12-01"},
        )
        assert agent.guardrail_ids == ["grd_example"]
        assert json.loads(_req(route).content)["guardrail_ids"] == ["grd_example"]
        assert _req(route).headers["orca-beta"] == "guardrails-2025-12-01"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_agent_update_can_clear_guardrail_ids(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/v1/agents/agent_123").mock(return_value=httpx2.Response(200, json=AGENT))
        client.agents.update("agent_123", guardrail_ids=None)
        assert json.loads(_req(route).content) == {"guardrail_ids": None}

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_core_agent_call_without_policy_field_does_not_probe(self, client: Orca, respx_mock: MockRouter) -> None:
        gate = _gate(respx_mock, client)
        respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json={**AGENT, "guardrail_ids": []}))
        client.agents.create(model="some-model", name="demo")
        assert gate.called is False

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_agent_policy_field_is_blocked_when_extension_is_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client, available=False)
        route = respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        with pytest.raises(ExtensionNotAvailableError, match="policy.runorca.ai"):
            client.agents.create(model="some-model", name="demo", guardrail_ids=[])
        assert route.called is False

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_session_override_gates_and_sends_guardrail_ids(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        client.sessions.create(
            environment_id="env_123",
            agent={"type": "agent_with_overrides", "id": "agent_123", "guardrail_ids": ["grd_example"]},
        )
        assert json.loads(_req(route).content)["agent"]["guardrail_ids"] == ["grd_example"]

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_session_reference_without_override_does_not_probe(self, client: Orca, respx_mock: MockRouter) -> None:
        gate = _gate(respx_mock, client)
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        client.sessions.create(environment_id="env_123", agent="agent_123")
        assert gate.called is False


class TestAsyncPolicyFields:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_agent_and_session_policy_fields(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        agent_route = respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        await async_client.agents.create(model="some-model", name="demo", guardrail_ids=["grd_example"])
        assert json.loads(_req(agent_route).content)["guardrail_ids"] == ["grd_example"]

        session_route = respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        await async_client.sessions.create(
            environment_id="env_123",
            agent={"type": "agent_with_overrides", "id": "agent_123", "guardrail_ids": ["grd_example"]},
        )
        assert json.loads(_req(session_route).content)["agent"]["guardrail_ids"] == ["grd_example"]
