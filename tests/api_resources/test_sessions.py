from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca
from tests.utils import assert_matches_type
from orca.pagination import SyncPageCursor, AsyncPageCursor
from orca.types.session import Session, DeletedSession

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

SESSION_AGENT: dict[str, Any] = {
    "id": "agent_123",
    "type": "agent",
    "name": "demo",
    "description": None,
    "version": 1,
    "model": {"id": "some-model"},
    "system": None,
    "tools": [],
    "mcp_servers": [],
    "skills": [],
    "multiagent": None,
}

SESSION: dict[str, Any] = {
    "id": "session_123",
    "type": "session",
    "agent": SESSION_AGENT,
    "environment_id": "env_123",
    "vault_ids": [],
    "status": "running",
    "title": None,
    "stats": {},
    "outcome_evaluations": [],
    "usage": {},
    "resources": [],
    "metadata": {},
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


def _page(*sessions: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(sessions), "next_page": next_page}


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        session = client.sessions.create(environment_id="env_123", agent="agent_123")
        assert_matches_type(Session, session, path=["response"])
        assert _req(route).method == "POST"
        assert json.loads(_req(route).content) == {"environment_id": "env_123", "agent": "agent_123"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        session = client.sessions.create(
            environment_id="env_123",
            agent={"type": "agent_with_overrides", "id": "agent_123", "version": 2, "model": "some-model"},
            vault_ids=["vault_1"],
            title="t",
            metadata={"team": "core"},
            resources=[{"type": "file", "file_id": "file_1", "mount_path": "/data"}],
            initial_events=[{"type": "user.message", "content": [{"type": "text", "text": "hi"}]}],
        )
        assert_matches_type(Session, session, path=["response"])
        body = json.loads(_req(route).content)
        assert body["agent"] == {
            "type": "agent_with_overrides",
            "id": "agent_123",
            "version": 2,
            "model": "some-model",
        }
        assert body["resources"] == [{"type": "file", "file_id": "file_1", "mount_path": "/data"}]
        assert body["initial_events"][0]["content"] == [{"type": "text", "text": "hi"}]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_agent_id_compat_form(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        client.sessions.create(environment_id="env_123", agent_id="agent_123")
        assert json.loads(_req(route).content) == {"environment_id": "env_123", "agent_id": "agent_123"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        response = client.sessions.with_raw_response.create(environment_id="env_123", agent="agent_123")
        assert response.is_closed is True
        assert_matches_type(Session, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        with client.sessions.with_streaming_response.create(environment_id="env_123", agent="agent_123") as response:
            assert not response.is_closed
            assert_matches_type(Session, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123").mock(return_value=httpx2.Response(200, json=SESSION))
        assert_matches_type(Session, client.sessions.retrieve("session_123"), path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=SESSION))
        client.sessions.retrieve("a b/c")
        assert "/v1/sessions/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123").mock(return_value=httpx2.Response(200, json=SESSION))
        client.sessions.update(
            "session_123",
            title="renamed",
            metadata={"drop": None},
            agent={"tools": [{"type": "agent_toolset"}]},
        )
        body = json.loads(_req(route).content)
        assert body == {
            "agent": {"tools": [{"type": "agent_toolset"}]},
            "title": "renamed",
            "metadata": {"drop": None},
        }

    @parametrize
    def test_path_params_update(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.update("", title="t")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions").mock(return_value=httpx2.Response(200, json=_page(SESSION)))
        assert_matches_type(SyncPageCursor[Session], client.sessions.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions").mock(return_value=httpx2.Response(200, json=_page(SESSION)))
        client.sessions.list(agent_id="agent_123", limit=20, page="tok", include_archived=True)
        params = _req(route).url.params
        assert params["agent_id"] == "agent_123"
        assert params["limit"] == "20"
        assert params["page"] == "tok"
        assert params["include_archived"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**SESSION, "id": "session_456"}
        respx_mock.get("/v1/sessions").mock(
            side_effect=[
                httpx2.Response(200, json=_page(SESSION, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [s.id for s in client.sessions.list()]
        assert ids == ["session_123", "session_456"]
        assert _req(respx_mock, 1).url.params["page"] == "cursor-2"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        tombstone = {"id": "session_123", "type": "session_deleted"}
        route = respx_mock.delete("/v1/sessions/session_123").mock(return_value=httpx2.Response(200, json=tombstone))
        assert_matches_type(DeletedSession, client.sessions.delete("session_123"), path=["response"])
        assert _req(route).method == "DELETE"

    @parametrize
    def test_path_params_delete(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.delete("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_archive(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/archive").mock(
            return_value=httpx2.Response(200, json=SESSION)
        )
        assert_matches_type(Session, client.sessions.archive("session_123"), path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    def test_path_params_archive(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.archive("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions").mock(return_value=httpx2.Response(200, json=_page()))
        client.sessions.list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        session = await async_client.sessions.create(environment_id="env_123", agent="agent_123")
        assert_matches_type(Session, session, path=["response"])
        assert json.loads(_req(route).content) == {"environment_id": "env_123", "agent": "agent_123"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        response = await async_client.sessions.with_raw_response.create(environment_id="env_123", agent="agent_123")
        assert response.is_closed is True
        assert_matches_type(Session, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        async with async_client.sessions.with_streaming_response.create(
            environment_id="env_123", agent="agent_123"
        ) as response:
            assert not response.is_closed
            assert_matches_type(Session, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123").mock(return_value=httpx2.Response(200, json=SESSION))
        assert_matches_type(Session, await async_client.sessions.retrieve("session_123"), path=["response"])

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123").mock(return_value=httpx2.Response(200, json=SESSION))
        await async_client.sessions.update("session_123", title="renamed", metadata={"drop": None})
        assert json.loads(_req(route).content) == {"title": "renamed", "metadata": {"drop": None}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions").mock(return_value=httpx2.Response(200, json=_page(SESSION)))
        assert_matches_type(AsyncPageCursor[Session], await async_client.sessions.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**SESSION, "id": "session_456"}
        respx_mock.get("/v1/sessions").mock(
            side_effect=[
                httpx2.Response(200, json=_page(SESSION, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [s.id async for s in async_client.sessions.list()]
        assert ids == ["session_123", "session_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        tombstone = {"id": "session_123", "type": "session_deleted"}
        respx_mock.delete("/v1/sessions/session_123").mock(return_value=httpx2.Response(200, json=tombstone))
        assert_matches_type(DeletedSession, await async_client.sessions.delete("session_123"), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_archive(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions/session_123/archive").mock(return_value=httpx2.Response(200, json=SESSION))
        assert_matches_type(Session, await async_client.sessions.archive("session_123"), path=["response"])
