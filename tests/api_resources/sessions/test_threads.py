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
from orca.resources.sessions import ThreadEvents, AsyncThreadEvents
from orca.types.session_event import SessionEvent
from orca.types.session_thread import SessionThread

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

THREAD_AGENT: dict[str, Any] = {
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
}

THREAD: dict[str, Any] = {
    "id": "sth_123",
    "type": "session_thread",
    "session_id": "session_123",
    "agent": THREAD_AGENT,
    "parent_thread_id": None,
    "status": "running",
    "stats": None,
    "usage": None,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
    "archived_at": None,
}

EVENT: dict[str, Any] = {"id": "evt_123", "type": "agent.message", "processed_at": None}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*items: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(items), "next_page": next_page}


def _sse(*events: dict[str, Any]) -> bytes:
    return b"".join(f"event: {e['type']}\ndata: {json.dumps(e)}\n\n".encode() for e in events)


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/threads/sth_123").mock(
            return_value=httpx2.Response(200, json=THREAD)
        )
        thread = client.sessions.threads.retrieve("session_123", "sth_123")
        assert_matches_type(SessionThread, thread, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.threads.with_raw_response.retrieve("", "sth_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.sessions.threads.with_raw_response.retrieve("session_123", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/threads").mock(return_value=httpx2.Response(200, json=_page(THREAD)))
        assert_matches_type(
            SyncPageCursor[SessionThread], client.sessions.threads.list("session_123"), path=["response"]
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/threads").mock(
            return_value=httpx2.Response(200, json=_page(THREAD))
        )
        client.sessions.threads.list("session_123", limit=3, page="tok")
        params = _req(route).url.params
        assert params["limit"] == "3"
        assert params["page"] == "tok"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**THREAD, "id": "sth_456"}
        respx_mock.get("/v1/sessions/session_123/threads").mock(
            side_effect=[
                httpx2.Response(200, json=_page(THREAD, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [t.id for t in client.sessions.threads.list("session_123")] == ["sth_123", "sth_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_archive(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/threads/sth_123/archive").mock(
            return_value=httpx2.Response(200, json=THREAD)
        )
        assert_matches_type(SessionThread, client.sessions.threads.archive("session_123", "sth_123"), path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    def test_path_params_archive(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.sessions.threads.with_raw_response.archive("session_123", "")

    @parametrize
    def test_events_sub_resource_is_wired(self, client: Orca) -> None:
        assert isinstance(client.sessions.threads.events, ThreadEvents)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_events_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/threads/sth_123/events").mock(
            return_value=httpx2.Response(200, json=_page(EVENT))
        )
        page = client.sessions.threads.events.list("session_123", "sth_123", limit=2, page="tok")
        assert_matches_type(SyncPageCursor[SessionEvent], page, path=["response"])
        params = _req(route).url.params
        assert params["limit"] == "2"
        assert params["page"] == "tok"

    @parametrize
    def test_events_path_params_list(self, client: Orca) -> None:
        events = client.sessions.threads.events
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            events.with_raw_response.list("", "sth_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            events.with_raw_response.list("session_123", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_events_method_stream_hangs_off_thread_not_events(self, client: Orca, respx_mock: MockRouter) -> None:
        """The thread stream is `/threads/{id}/stream`, not `/threads/{id}/events/stream`."""
        route = respx_mock.get("/v1/sessions/session_123/threads/sth_123/stream").mock(
            return_value=httpx2.Response(200, headers={"Content-Type": "text/event-stream"}, content=_sse(EVENT))
        )
        stream = client.sessions.threads.events.stream("session_123", "sth_123")
        assert [e.id for e in stream] == ["evt_123"]
        assert _req(route).url.path == "/v1/sessions/session_123/threads/sth_123/stream"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_events_method_stream_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/threads/sth_123/stream").mock(
            return_value=httpx2.Response(200, headers={"Content-Type": "text/event-stream"}, content=_sse(EVENT))
        )
        list(
            client.sessions.threads.events.stream(
                "session_123", "sth_123", from_cursor="evt_prev", event_deltas="agent.thinking"
            )
        )
        params = _req(route).url.params
        assert params["from_cursor"] == "evt_prev"
        assert params.get_list("event_deltas") == ["agent.thinking"]

    @parametrize
    def test_events_path_params_stream(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.sessions.threads.events.stream("session_123", "")


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/threads/sth_123").mock(return_value=httpx2.Response(200, json=THREAD))
        assert_matches_type(
            SessionThread,
            await async_client.sessions.threads.retrieve("session_123", "sth_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/threads").mock(return_value=httpx2.Response(200, json=_page(THREAD)))
        assert_matches_type(
            AsyncPageCursor[SessionThread],
            await async_client.sessions.threads.list("session_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_archive(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions/session_123/threads/sth_123/archive").mock(
            return_value=httpx2.Response(200, json=THREAD)
        )
        assert_matches_type(
            SessionThread,
            await async_client.sessions.threads.archive("session_123", "sth_123"),
            path=["response"],
        )

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.sessions.threads.with_raw_response.archive("session_123", "")

    @parametrize
    def test_events_sub_resource_is_wired(self, async_client: AsyncOrca) -> None:
        assert isinstance(async_client.sessions.threads.events, AsyncThreadEvents)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_events_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/threads/sth_123/events").mock(
            return_value=httpx2.Response(200, json=_page(EVENT))
        )
        assert_matches_type(
            AsyncPageCursor[SessionEvent],
            await async_client.sessions.threads.events.list("session_123", "sth_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_events_method_stream(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/threads/sth_123/stream").mock(
            return_value=httpx2.Response(200, headers={"Content-Type": "text/event-stream"}, content=_sse(EVENT))
        )
        stream = await async_client.sessions.threads.events.stream("session_123", "sth_123")
        assert [e.id async for e in stream] == ["evt_123"]
        assert _req(route).url.path == "/v1/sessions/session_123/threads/sth_123/stream"

    @parametrize
    async def test_events_path_params_stream(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.threads.events.stream("", "sth_123")
