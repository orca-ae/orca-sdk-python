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
from orca.types.session_event import SessionEvent
from orca.types.session_event_send_response import SessionEventSendResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

EVENT: dict[str, Any] = {
    "id": "evt_123",
    "type": "agent.message",
    "processed_at": None,
    "content": [{"type": "text", "text": "hello"}],
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*events: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(events), "next_page": next_page}


def _sse(*events: dict[str, Any]) -> bytes:
    return b"".join(f"event: {e['type']}\ndata: {json.dumps(e)}\n\n".encode() for e in events)


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/events").mock(return_value=httpx2.Response(200, json=_page(EVENT)))
        assert_matches_type(SyncPageCursor[SessionEvent], client.sessions.events.list("session_123"), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/events").mock(
            return_value=httpx2.Response(200, json=_page(EVENT))
        )
        client.sessions.events.list(
            "session_123",
            limit=10,
            page="tok",
            created_at_gt="2026-01-01T00:00:00Z",
            created_at_gte="2026-01-02T00:00:00Z",
            created_at_lt="2026-02-01T00:00:00Z",
            created_at_lte="2026-02-02T00:00:00Z",
            order="asc",
            types=["agent.message", "user.message"],
            subpath="sub",
        )
        params = _req(route).url.params
        assert params["limit"] == "10"
        assert params["page"] == "tok"
        assert params["created_at[gt]"] == "2026-01-01T00:00:00Z"
        assert params["created_at[gte]"] == "2026-01-02T00:00:00Z"
        assert params["created_at[lt]"] == "2026-02-01T00:00:00Z"
        assert params["created_at[lte]"] == "2026-02-02T00:00:00Z"
        assert params["order"] == "asc"
        assert params.get_list("types") == ["agent.message", "user.message"]
        assert params["subpath"] == "sub"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_accepts_a_single_type(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/events").mock(
            return_value=httpx2.Response(200, json=_page(EVENT))
        )
        client.sessions.events.list("session_123", types="agent.message")
        assert _req(route).url.params.get_list("types") == ["agent.message"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**EVENT, "id": "evt_456"}
        respx_mock.get("/v1/sessions/session_123/events").mock(
            side_effect=[
                httpx2.Response(200, json=_page(EVENT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [e.id for e in client.sessions.events.list("session_123")] == ["evt_123", "evt_456"]

    @parametrize
    def test_path_params_list(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.events.with_raw_response.list("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_send(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/events").mock(
            return_value=httpx2.Response(200, json={"data": [EVENT]})
        )
        response = client.sessions.events.send(
            "session_123",
            events=[{"type": "user.message", "content": [{"type": "text", "text": "hi"}]}],
        )
        assert_matches_type(SessionEventSendResponse, response, path=["response"])
        assert json.loads(_req(route).content) == {
            "events": [{"type": "user.message", "content": [{"type": "text", "text": "hi"}]}]
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_send_every_event_kind(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/events").mock(
            return_value=httpx2.Response(200, json={"data": []})
        )
        client.sessions.events.send(
            "session_123",
            events=[
                {"type": "user.interrupt", "session_thread_id": "sth_1"},
                {"type": "user.tool_confirmation", "tool_use_id": "tu_1", "result": "deny", "deny_message": "no"},
                {"type": "user.custom_tool_result", "custom_tool_use_id": "ctu_1", "is_error": True},
                {
                    "type": "user.define_outcome",
                    "description": "d",
                    "rubric": {"type": "file", "file_id": "file_1"},
                    "max_iterations": 3,
                },
                {"type": "user.tool_result", "tool_use_id": "tu_2", "content": []},
                {"type": "system.message", "content": [{"type": "text", "text": "sys"}]},
            ],
        )
        body = json.loads(_req(route).content)
        assert [e["type"] for e in body["events"]] == [
            "user.interrupt",
            "user.tool_confirmation",
            "user.custom_tool_result",
            "user.define_outcome",
            "user.tool_result",
            "system.message",
        ]

    @parametrize
    def test_path_params_send(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.events.with_raw_response.send("", events=[])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_stream(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/events/stream").mock(
            return_value=httpx2.Response(200, headers={"Content-Type": "text/event-stream"}, content=_sse(EVENT))
        )
        stream = client.sessions.events.stream("session_123")
        events = list(stream)
        assert [e.id for e in events] == ["evt_123"]
        assert_matches_type(SessionEvent, events[0], path=["response"])
        assert "/v1/sessions/session_123/events/stream" in str(_req(route).url)
        assert _req(route).headers["accept"] == "text/event-stream"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_stream_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/events/stream").mock(
            return_value=httpx2.Response(200, headers={"Content-Type": "text/event-stream"}, content=_sse(EVENT))
        )
        list(
            client.sessions.events.stream(
                "session_123",
                from_cursor="evt_prev",
                subpath="sub",
                event_deltas=["agent.message", "agent.thinking"],
                extra_headers={"Accept": "text/event-stream; replay=all"},
            )
        )
        params = _req(route).url.params
        assert params["from_cursor"] == "evt_prev"
        assert params["subpath"] == "sub"
        assert params.get_list("event_deltas") == ["agent.message", "agent.thinking"]
        assert _req(route).headers["accept"] == "text/event-stream; replay=all"

    @parametrize
    def test_path_params_stream(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.events.stream("")


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/events").mock(return_value=httpx2.Response(200, json=_page(EVENT)))
        assert_matches_type(
            AsyncPageCursor[SessionEvent],
            await async_client.sessions.events.list("session_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**EVENT, "id": "evt_456"}
        respx_mock.get("/v1/sessions/session_123/events").mock(
            side_effect=[
                httpx2.Response(200, json=_page(EVENT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [e.id async for e in async_client.sessions.events.list("session_123")]
        assert ids == ["evt_123", "evt_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_send(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/events").mock(
            return_value=httpx2.Response(200, json={"data": [EVENT]})
        )
        response = await async_client.sessions.events.send(
            "session_123",
            events=[{"type": "user.message", "content": [{"type": "text", "text": "hi"}]}],
        )
        assert_matches_type(SessionEventSendResponse, response, path=["response"])
        assert json.loads(_req(route).content)["events"][0]["type"] == "user.message"

    @parametrize
    async def test_path_params_send(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.events.with_raw_response.send("", events=[])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_stream(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/events/stream").mock(
            return_value=httpx2.Response(200, headers={"Content-Type": "text/event-stream"}, content=_sse(EVENT))
        )
        stream = await async_client.sessions.events.stream("session_123")
        events = [e async for e in stream]
        assert [e.id for e in events] == ["evt_123"]
        assert _req(route).headers["accept"] == "text/event-stream"

    @parametrize
    async def test_path_params_stream(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.events.stream("")
