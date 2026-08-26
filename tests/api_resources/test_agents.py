from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca
from orca.types import Agent
from tests.utils import assert_matches_type
from orca.pagination import SyncPageCursor, AsyncPageCursor

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
    "multiagent": None,
    "metadata": {},
    "version": 1,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
    "archived_at": None,
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*agents: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(agents), "next_page": next_page}


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        agent = client.agents.create(model="some-model", name="demo")
        assert_matches_type(Agent, agent, path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        import json

        route = respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        agent = client.agents.create(
            model={"id": "some-model", "effort": "high"},
            name="demo",
            description="d",
            system="s",
            mcp_servers=[{"name": "srv", "url": "https://mcp.test"}],
            tools=[{"type": "agent_toolset"}],
            skills=[{"type": "custom", "skill_id": "skill_1"}],
            metadata={"team": "core"},
            multiagent={"type": "coordinator", "agents": ["agent_2"]},
        )
        assert_matches_type(Agent, agent, path=["response"])
        body = json.loads(_req(route).content)
        assert body["model"] == {"id": "some-model", "effort": "high"}
        assert body["metadata"] == {"team": "core"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        response = client.agents.with_raw_response.create(model="m", name="demo")
        assert response.is_closed is True
        assert_matches_type(Agent, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        with client.agents.with_streaming_response.create(model="m", name="demo") as response:
            assert not response.is_closed
            assert_matches_type(Agent, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/agents/agent_123").mock(return_value=httpx2.Response(200, json=AGENT))
        assert_matches_type(Agent, client.agents.retrieve("agent_123"), path=["response"])
        assert _req(route).url.params.get("version") is None

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_with_version(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/agents/agent_123").mock(return_value=httpx2.Response(200, json=AGENT))
        client.agents.retrieve("agent_123", version=3)
        assert _req(route).url.params["version"] == "3"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=AGENT))
        client.agents.retrieve("a b/c")
        assert "/v1/agents/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        import json

        route = respx_mock.post("/v1/agents/agent_123").mock(return_value=httpx2.Response(200, json=AGENT))
        client.agents.update("agent_123", version=1, name="renamed", metadata={"drop": None})
        body = json.loads(_req(route).content)
        assert body == {"version": 1, "name": "renamed", "metadata": {"drop": None}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/agents").mock(return_value=httpx2.Response(200, json=_page(AGENT)))
        assert_matches_type(SyncPageCursor[Agent], client.agents.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/agents").mock(return_value=httpx2.Response(200, json=_page(AGENT)))
        client.agents.list(limit=20, page="tok", include_archived=True)
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["page"] == "tok"
        assert params["include_archived"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**AGENT, "id": "agent_456"}
        respx_mock.get("/v1/agents").mock(
            side_effect=[
                httpx2.Response(200, json=_page(AGENT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [a.id for a in client.agents.list()]
        assert ids == ["agent_123", "agent_456"]
        assert _req(respx_mock, 1).url.params["page"] == "cursor-2"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_archive(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/agents/agent_123/archive").mock(return_value=httpx2.Response(200, json=AGENT))
        assert_matches_type(Agent, client.agents.archive("agent_123"), path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/agents").mock(return_value=httpx2.Response(200, json=_page()))
        client.agents.list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_versions_list(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/agents/agent_123/versions").mock(
            return_value=httpx2.Response(200, json=_page(AGENT))
        )
        assert_matches_type(SyncPageCursor[Agent], client.agents.versions.list("agent_123"), path=["response"])
        assert route.call_count == 1

    @parametrize
    def test_versions_path_params(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.versions.with_raw_response.list("")


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        agent = await async_client.agents.create(model="some-model", name="demo")
        assert_matches_type(Agent, agent, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        response = await async_client.agents.with_raw_response.create(model="m", name="demo")
        assert response.is_closed is True
        assert_matches_type(Agent, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json=AGENT))
        async with async_client.agents.with_streaming_response.create(model="m", name="demo") as response:
            assert not response.is_closed
            assert_matches_type(Agent, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/agents/agent_123").mock(return_value=httpx2.Response(200, json=AGENT))
        assert_matches_type(Agent, await async_client.agents.retrieve("agent_123"), path=["response"])

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/agents").mock(return_value=httpx2.Response(200, json=_page(AGENT)))
        assert_matches_type(AsyncPageCursor[Agent], await async_client.agents.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**AGENT, "id": "agent_456"}
        respx_mock.get("/v1/agents").mock(
            side_effect=[
                httpx2.Response(200, json=_page(AGENT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [a.id async for a in async_client.agents.list()]
        assert ids == ["agent_123", "agent_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_archive(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/agents/agent_123/archive").mock(return_value=httpx2.Response(200, json=AGENT))
        assert_matches_type(Agent, await async_client.agents.archive("agent_123"), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_versions_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/agents/agent_123/versions").mock(return_value=httpx2.Response(200, json=_page(AGENT)))
        assert_matches_type(
            AsyncPageCursor[Agent], await async_client.agents.versions.list("agent_123"), path=["response"]
        )
