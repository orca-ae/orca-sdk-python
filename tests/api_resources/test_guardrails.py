from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from orca.types import Guardrail, DeletedGuardrail, GuardrailTypeList
from tests.utils import assert_matches_type
from orca.pagination import SyncPageCursor, AsyncPageCursor

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

GUARDRAIL: dict[str, Any] = {
    "id": "grd_example",
    "type": "guardrail",
    "name": "Protect production",
    "description": "Blocks risky tool calls",
    "enabled": True,
    "phases": ["tool_call"],
    "scope": "workspace",
    "rule": {"kind": "builtin", "builtin": "block_tools", "params": {"tools": ["shell"]}},
    "metadata": {"owner": "platform"},
    "archived_at": None,
    "created_at": "2026-09-01T00:00:00Z",
    "updated_at": "2026-09-01T00:00:00Z",
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    return cast("httpx2.Request", route.calls[index].request)


def _gate(respx_mock: MockRouter, client: Orca | AsyncOrca, *, available: bool = True) -> Any:
    client._extension_groups.clear()
    groups = [{"name": "policy.runorca.ai"}] if available else []
    return respx_mock.get("/apis").mock(
        return_value=httpx2.Response(200, json={"kind": "APIGroupList", "groups": groups})
    )


class TestGuardrails:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_create_sends_complete_wire_shape(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/policy.runorca.ai/v1/guardrails").mock(
            return_value=httpx2.Response(201, json=GUARDRAIL)
        )
        result = client.guardrails.create(
            name="Protect production",
            description=None,
            enabled=True,
            phases=["tool_call"],
            scope="explicit",
            rule={
                "kind": "expression",
                "expression": 'event.tool.name != "shell"',
                "on_false": "ask",
                "reason": "Approval required",
            },
            metadata={"owner": "platform"},
            extra_headers={"X-Test": "create"},
        )
        assert_matches_type(Guardrail, result, path=["response"])
        assert json.loads(_req(route).content) == {
            "name": "Protect production",
            "description": None,
            "enabled": True,
            "phases": ["tool_call"],
            "scope": "explicit",
            "rule": {
                "kind": "expression",
                "expression": 'event.tool.name != "shell"',
                "on_false": "ask",
                "reason": "Approval required",
            },
            "metadata": {"owner": "platform"},
        }
        assert _req(route).headers["x-test"] == "create"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_uses_cursor_and_archive_filter(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/policy.runorca.ai/v1/guardrails").mock(
            return_value=httpx2.Response(200, json={"data": [GUARDRAIL], "next_page": None})
        )
        page = client.guardrails.list(limit=25, page="next", include_archived=True)
        assert_matches_type(SyncPageCursor[Guardrail], page, path=["response"])
        assert _req(route).url.params["limit"] == "25"
        assert _req(route).url.params["page"] == "next"
        assert _req(route).url.params["include_archived"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_update_archive_and_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        item = respx_mock.route(path__regex=r"/apis/policy\.runorca\.ai/v1/guardrails/.*").mock(
            return_value=httpx2.Response(200, json=GUARDRAIL)
        )
        client.guardrails.retrieve("grd/with space")
        assert str(_req(item).url).endswith("/apis/policy.runorca.ai/v1/guardrails/grd%2Fwith%20space")

        client.guardrails.update("grd_example", enabled=False, metadata={"owner": None})
        assert _req(item, 1).method == "POST"
        assert json.loads(_req(item, 1).content) == {"enabled": False, "metadata": {"owner": None}}

        client.guardrails.archive("grd_example")
        assert _req(item, 2).url.path.endswith("/grd_example/archive")

        item.mock(return_value=httpx2.Response(200, json={"id": "grd_example", "type": "guardrail_deleted"}))
        deleted = client.guardrails.delete("grd_example")
        assert_matches_type(DeletedGuardrail, deleted, path=["response"])
        assert _req(item, 3).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_types_maps_wire_aliases(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/policy.runorca.ai/v1/guardrailtypes").mock(
            return_value=httpx2.Response(
                200,
                json={
                    "data": [
                        {
                            "name": "rate_limit",
                            "title": "Rate limit",
                            "description": "Limits requests",
                            "phases": ["request"],
                            "stateful": True,
                            "stateScope": "subject_window",
                            "verdicts": ["deny"],
                            "paramsSchema": {"type": "object"},
                        }
                    ]
                },
            )
        )
        result = client.guardrails.list_types()
        assert_matches_type(GuardrailTypeList, result, path=["response"])
        assert result.data[0].state_scope == "subject_window"
        assert result.data[0].params_schema == {"type": "object"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_and_streaming_wrappers(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/policy.runorca.ai/v1/guardrails/grd_example").mock(
            return_value=httpx2.Response(200, json=GUARDRAIL)
        )
        raw = client.guardrails.with_raw_response.retrieve("grd_example")
        assert_matches_type(Guardrail, raw.parse(), path=["response"])
        with client.guardrails.with_streaming_response.retrieve("grd_example") as streamed:
            assert_matches_type(Guardrail, streamed.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_before_business_request(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client, available=False)
        route = respx_mock.get("/apis/policy.runorca.ai/v1/guardrails/grd_example").mock(
            return_value=httpx2.Response(200, json=GUARDRAIL)
        )
        with pytest.raises(ExtensionNotAvailableError, match="policy.runorca.ai"):
            client.guardrails.retrieve("grd_example")
        assert route.called is False


class TestAsyncGuardrails:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_create_and_paginated_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.post("/apis/policy.runorca.ai/v1/guardrails").mock(return_value=httpx2.Response(201, json=GUARDRAIL))
        created = await async_client.guardrails.create(
            name="Protect production", rule={"kind": "builtin", "builtin": "block_tools"}
        )
        assert_matches_type(Guardrail, created, path=["response"])

        respx_mock.get("/apis/policy.runorca.ai/v1/guardrails").mock(
            return_value=httpx2.Response(200, json={"data": [GUARDRAIL], "next_page": None})
        )
        page = await async_client.guardrails.list(limit=10)
        assert_matches_type(AsyncPageCursor[Guardrail], page, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_paginated_raw_and_streaming_wrappers(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/policy.runorca.ai/v1/guardrails").mock(
            return_value=httpx2.Response(200, json={"data": [GUARDRAIL], "next_page": None})
        )
        raw = await async_client.guardrails.with_raw_response.list()
        assert_matches_type(AsyncPageCursor[Guardrail], await raw.parse(), path=["response"])
        async with async_client.guardrails.with_streaming_response.list() as streamed:
            assert_matches_type(AsyncPageCursor[Guardrail], await streamed.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_paginated_list_is_gated_before_request(
        self, async_client: AsyncOrca, respx_mock: MockRouter
    ) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get("/apis/policy.runorca.ai/v1/guardrails").mock(
            return_value=httpx2.Response(200, json={"data": [], "next_page": None})
        )
        with pytest.raises(ExtensionNotAvailableError, match="policy.runorca.ai"):
            await async_client.guardrails.list()
        assert route.called is False
