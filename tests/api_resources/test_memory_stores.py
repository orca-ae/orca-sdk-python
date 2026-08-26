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
from orca.types.memory import Memory, MemoryPrefix, DeletedMemory, MemoryListItem
from orca.types.memory_store import MemoryStore, DeletedMemoryStore
from orca.types.memory_version import MemoryVersion

# The resources are constructed against the client directly rather than reached
# through `client.memory_stores`, which is what the client mount will do once the
# mount lands in `_client.py`.
from orca.resources.memory_stores import MemoryStores, AsyncMemoryStores

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

MEMORY_STORE: dict[str, Any] = {
    "id": "mems_123",
    "type": "memory_store",
    "name": "project-notes",
    "description": None,
    "metadata": {},
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
    "archived_at": None,
}

DELETED_MEMORY_STORE: dict[str, Any] = {"id": "mems_123", "type": "memory_store_deleted"}

MEMORY: dict[str, Any] = {
    "id": "mem_123",
    "content_sha256": "a" * 64,
    "content_size_bytes": 13,
    "created_at": "2026-01-01T00:00:00Z",
    "memory_store_id": "mems_123",
    "memory_version_id": "memver_123",
    "path": "notes/todo.md",
    "type": "memory",
    "updated_at": "2026-01-01T00:00:00Z",
    "content": "Remember this",
}

MEMORY_PREFIX: dict[str, Any] = {"path": "notes/", "type": "memory_prefix"}

DELETED_MEMORY: dict[str, Any] = {"id": "mem_123", "type": "memory_deleted"}

MEMORY_VERSION: dict[str, Any] = {
    "id": "memver_123",
    "created_at": "2026-01-01T00:00:00Z",
    "memory_id": "mem_123",
    "memory_store_id": "mems_123",
    "operation": "created",
    "type": "memory_version",
    "content": "Remember this",
    "content_sha256": "a" * 64,
    "content_size_bytes": 13,
    "created_by": {"type": "api_actor", "api_key_id": "key_1"},
    "path": "notes/todo.md",
    "redacted_at": None,
    "redacted_by": None,
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*items: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(items), "next_page": next_page}


class TestMemoryStores:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        store = MemoryStores(client).create(name="project-notes")
        assert_matches_type(MemoryStore, store, path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        MemoryStores(client).create(name="project-notes", description="d", metadata={"team": "core"})
        assert json.loads(_req(route).content) == {
            "name": "project-notes",
            "description": "d",
            "metadata": {"team": "core"},
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        response = MemoryStores(client).with_raw_response.create(name="project-notes")
        assert response.is_closed is True
        assert_matches_type(MemoryStore, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        with MemoryStores(client).with_streaming_response.create(name="project-notes") as response:
            assert not response.is_closed
            assert_matches_type(MemoryStore, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores/mems_123").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        assert_matches_type(MemoryStore, MemoryStores(client).retrieve("mems_123"), path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            MemoryStores(client).with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        MemoryStores(client).retrieve("a b/c")
        assert "/v1/memory_stores/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores/mems_123").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        MemoryStores(client).update("mems_123", name="renamed", description=None, metadata={"drop": None})
        assert _req(route).method == "POST"
        assert json.loads(_req(route).content) == {
            "name": "renamed",
            "description": None,
            "metadata": {"drop": None},
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=_page(MEMORY_STORE)))
        assert_matches_type(SyncPageCursor[MemoryStore], MemoryStores(client).list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=_page(MEMORY_STORE)))
        MemoryStores(client).list(limit=20, page="tok", include_archived=True)
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["page"] == "tok"
        assert params["include_archived"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**MEMORY_STORE, "id": "mems_456"}
        respx_mock.get("/v1/memory_stores").mock(
            side_effect=[
                httpx2.Response(200, json=_page(MEMORY_STORE, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [s.id for s in MemoryStores(client).list()] == ["mems_123", "mems_456"]
        assert _req(respx_mock, 1).url.params["page"] == "cursor-2"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/memory_stores/mems_123").mock(
            return_value=httpx2.Response(200, json=DELETED_MEMORY_STORE)
        )
        deleted = MemoryStores(client).delete("mems_123")
        assert_matches_type(DeletedMemoryStore, deleted, path=["response"])
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_archive(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores/mems_123/archive").mock(
            return_value=httpx2.Response(200, json=MEMORY_STORE)
        )
        assert_matches_type(MemoryStore, MemoryStores(client).archive("mems_123"), path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=_page()))
        MemoryStores(client).list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"

    # ---- memories ----------------------------------------------------------

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memories_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/memory_stores/mems_123/memories").mock(
            return_value=httpx2.Response(200, json=_page(MEMORY, MEMORY_PREFIX))
        )
        page = MemoryStores(client).memories.list("mems_123")
        assert_matches_type(SyncPageCursor[MemoryListItem], page, path=["response"])
        entries = list(page)
        assert isinstance(entries[0], Memory)
        assert isinstance(entries[1], MemoryPrefix)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memories_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores/mems_123/memories").mock(
            return_value=httpx2.Response(200, json=_page(MEMORY))
        )
        MemoryStores(client).memories.list("mems_123", limit=5, page="tok", depth=1, path_prefix="notes/", view="full")
        params = _req(route).url.params
        assert params["limit"] == "5"
        assert params["page"] == "tok"
        assert params["depth"] == "1"
        assert params["path_prefix"] == "notes/"
        assert params["view"] == "full"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memories_create_splits_body_and_query(self, client: Orca, respx_mock: MockRouter) -> None:
        """`view` is a query parameter; only `path` and `content` are sent as the body."""
        route = respx_mock.post("/v1/memory_stores/mems_123/memories").mock(
            return_value=httpx2.Response(200, json=MEMORY)
        )
        memory = MemoryStores(client).memories.create(
            "mems_123", path="notes/todo.md", content="Remember this", view="full"
        )
        assert_matches_type(Memory, memory, path=["response"])
        request = _req(route)
        assert json.loads(request.content) == {"path": "notes/todo.md", "content": "Remember this"}
        assert request.url.params["view"] == "full"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memories_create_null_content(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores/mems_123/memories").mock(
            return_value=httpx2.Response(200, json=MEMORY)
        )
        MemoryStores(client).memories.create("mems_123", path="notes/todo.md", content=None)
        assert json.loads(_req(route).content) == {"path": "notes/todo.md", "content": None}
        assert _req(route).url.params.get("view") is None

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memories_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores/mems_123/memories/mem_123").mock(
            return_value=httpx2.Response(200, json=MEMORY)
        )
        memory = MemoryStores(client).memories.retrieve("mems_123", "mem_123", view="basic")
        assert_matches_type(Memory, memory, path=["response"])
        assert _req(route).url.params["view"] == "basic"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memories_update(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores/mems_123/memories/mem_123").mock(
            return_value=httpx2.Response(200, json=MEMORY)
        )
        MemoryStores(client).memories.update(
            "mems_123",
            "mem_123",
            content="Updated",
            path=None,
            precondition={"type": "content_sha256", "content_sha256": "b" * 64},
            view="full",
        )
        request = _req(route)
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "content": "Updated",
            "path": None,
            "precondition": {"type": "content_sha256", "content_sha256": "b" * 64},
        }
        assert request.url.params["view"] == "full"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memories_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/memory_stores/mems_123/memories/mem_123").mock(
            return_value=httpx2.Response(200, json=DELETED_MEMORY)
        )
        deleted = MemoryStores(client).memories.delete("mems_123", "mem_123", expected_content_sha256="c" * 64)
        assert_matches_type(DeletedMemory, deleted, path=["response"])
        assert _req(route).url.params["expected_content_sha256"] == "c" * 64

    @parametrize
    def test_memories_path_params(self, client: Orca) -> None:
        memories = MemoryStores(client).memories
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            memories.with_raw_response.retrieve("", "mem_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            memories.with_raw_response.retrieve("mems_123", "")

    # ---- memory versions ---------------------------------------------------

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memory_versions_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/memory_stores/mems_123/memory_versions").mock(
            return_value=httpx2.Response(200, json=_page(MEMORY_VERSION))
        )
        page = MemoryStores(client).memory_versions.list("mems_123")
        assert_matches_type(SyncPageCursor[MemoryVersion], page, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memory_versions_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores/mems_123/memory_versions").mock(
            return_value=httpx2.Response(200, json=_page(MEMORY_VERSION))
        )
        MemoryStores(client).memory_versions.list(
            "mems_123",
            limit=5,
            page="tok",
            memory_id="mem_123",
            api_key_id="key_1",
            operation="modified",
            created_at_gte="2026-01-01T00:00:00Z",
            created_at_lte="2026-02-01T00:00:00Z",
            view="full",
        )
        params = _req(route).url.params
        assert params["limit"] == "5"
        assert params["page"] == "tok"
        assert params["memory_id"] == "mem_123"
        assert params["api_key_id"] == "key_1"
        assert params["operation"] == "modified"
        assert params["created_at[gte]"] == "2026-01-01T00:00:00Z"
        assert params["created_at[lte]"] == "2026-02-01T00:00:00Z"
        assert params["view"] == "full"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memory_versions_list_omits_session_filter(self, client: Orca, respx_mock: MockRouter) -> None:
        """`session_id` is not portable, so the SDK never sends it."""
        route = respx_mock.get("/v1/memory_stores/mems_123/memory_versions").mock(
            return_value=httpx2.Response(200, json=_page(MEMORY_VERSION))
        )
        MemoryStores(client).memory_versions.list("mems_123")
        assert _req(route).url.params.get("session_id") is None

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memory_versions_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores/mems_123/memory_versions/memver_123").mock(
            return_value=httpx2.Response(200, json=MEMORY_VERSION)
        )
        version = MemoryStores(client).memory_versions.retrieve("mems_123", "memver_123", view="full")
        assert_matches_type(MemoryVersion, version, path=["response"])
        assert _req(route).url.params["view"] == "full"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_memory_versions_redact(self, client: Orca, respx_mock: MockRouter) -> None:
        redacted = {**MEMORY_VERSION, "content": None, "redacted_at": "2026-01-02T00:00:00Z"}
        route = respx_mock.post("/v1/memory_stores/mems_123/memory_versions/memver_123/redact").mock(
            return_value=httpx2.Response(200, json=redacted)
        )
        version = MemoryStores(client).memory_versions.redact("mems_123", "memver_123")
        assert_matches_type(MemoryVersion, version, path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    def test_memory_versions_path_params(self, client: Orca) -> None:
        versions = MemoryStores(client).memory_versions
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            versions.with_raw_response.redact("", "memver_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_version_id` but received ''"):
            versions.with_raw_response.redact("mems_123", "")


class TestAsyncMemoryStores:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        store = await AsyncMemoryStores(async_client).create(name="project-notes")
        assert_matches_type(MemoryStore, store, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        response = await AsyncMemoryStores(async_client).with_raw_response.create(name="project-notes")
        assert response.is_closed is True
        assert_matches_type(MemoryStore, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        async with AsyncMemoryStores(async_client).with_streaming_response.create(name="project-notes") as response:
            assert not response.is_closed
            assert_matches_type(MemoryStore, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/memory_stores/mems_123").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        store = await AsyncMemoryStores(async_client).retrieve("mems_123")
        assert_matches_type(MemoryStore, store, path=["response"])

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_store_id` but received ''"):
            await AsyncMemoryStores(async_client).with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores/mems_123").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        await AsyncMemoryStores(async_client).update("mems_123", name="renamed", metadata={"drop": None})
        assert json.loads(_req(route).content) == {"name": "renamed", "metadata": {"drop": None}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/memory_stores").mock(return_value=httpx2.Response(200, json=_page(MEMORY_STORE)))
        page = await AsyncMemoryStores(async_client).list()
        assert_matches_type(AsyncPageCursor[MemoryStore], page, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**MEMORY_STORE, "id": "mems_456"}
        respx_mock.get("/v1/memory_stores").mock(
            side_effect=[
                httpx2.Response(200, json=_page(MEMORY_STORE, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [s.id async for s in AsyncMemoryStores(async_client).list()]
        assert ids == ["mems_123", "mems_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/memory_stores/mems_123").mock(
            return_value=httpx2.Response(200, json=DELETED_MEMORY_STORE)
        )
        deleted = await AsyncMemoryStores(async_client).delete("mems_123")
        assert_matches_type(DeletedMemoryStore, deleted, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_archive(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/memory_stores/mems_123/archive").mock(return_value=httpx2.Response(200, json=MEMORY_STORE))
        store = await AsyncMemoryStores(async_client).archive("mems_123")
        assert_matches_type(MemoryStore, store, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_memories_create_splits_body_and_query(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/memory_stores/mems_123/memories").mock(
            return_value=httpx2.Response(200, json=MEMORY)
        )
        memory = await AsyncMemoryStores(async_client).memories.create(
            "mems_123", path="notes/todo.md", content="Remember this", view="full"
        )
        assert_matches_type(Memory, memory, path=["response"])
        request = _req(route)
        assert json.loads(request.content) == {"path": "notes/todo.md", "content": "Remember this"}
        assert request.url.params["view"] == "full"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_memories_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/memory_stores/mems_123/memories").mock(
            return_value=httpx2.Response(200, json=_page(MEMORY, MEMORY_PREFIX))
        )
        page = await AsyncMemoryStores(async_client).memories.list("mems_123")
        assert_matches_type(AsyncPageCursor[MemoryListItem], page, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_memories_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/memory_stores/mems_123/memories/mem_123").mock(
            return_value=httpx2.Response(200, json=DELETED_MEMORY)
        )
        deleted = await AsyncMemoryStores(async_client).memories.delete(
            "mems_123", "mem_123", expected_content_sha256="c" * 64
        )
        assert_matches_type(DeletedMemory, deleted, path=["response"])
        assert _req(route).url.params["expected_content_sha256"] == "c" * 64

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_memory_versions_list_with_all_params(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/memory_stores/mems_123/memory_versions").mock(
            return_value=httpx2.Response(200, json=_page(MEMORY_VERSION))
        )
        await AsyncMemoryStores(async_client).memory_versions.list(
            "mems_123",
            operation="deleted",
            created_at_gte="2026-01-01T00:00:00Z",
            view="basic",
        )
        params = _req(route).url.params
        assert params["operation"] == "deleted"
        assert params["created_at[gte]"] == "2026-01-01T00:00:00Z"
        assert params["view"] == "basic"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_memory_versions_redact(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        redacted = {**MEMORY_VERSION, "content": None, "redacted_at": "2026-01-02T00:00:00Z"}
        respx_mock.post("/v1/memory_stores/mems_123/memory_versions/memver_123/redact").mock(
            return_value=httpx2.Response(200, json=redacted)
        )
        version = await AsyncMemoryStores(async_client).memory_versions.redact("mems_123", "memver_123")
        assert_matches_type(MemoryVersion, version, path=["response"])

    @parametrize
    async def test_memory_versions_path_params(self, async_client: AsyncOrca) -> None:
        versions = AsyncMemoryStores(async_client).memory_versions
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_version_id` but received ''"):
            await versions.with_raw_response.retrieve("mems_123", "")
