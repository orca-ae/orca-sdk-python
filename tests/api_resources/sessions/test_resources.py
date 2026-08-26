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
from orca.types.session_resource import (
    SessionResource,
    SessionFileResource,
    DeletedSessionResource,
    SessionRepositoryResource,
    SessionMemoryStoreResource,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

FILE_RESOURCE: dict[str, Any] = {
    "id": "sres_123",
    "type": "file",
    "file_id": "file_123",
    "mount_path": "/data",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}

REPO_RESOURCE: dict[str, Any] = {
    "id": "sres_456",
    "type": "github_repository",
    "mount_path": "/repo",
    "url": "https://example.test/org/repo",
    "checkout": {"type": "branch", "name": "main"},
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}

MEMORY_RESOURCE: dict[str, Any] = {
    "type": "memory_store",
    "memory_store_id": "mems_123",
    "access": "read_write",
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*resources: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(resources), "next_page": next_page}


class TestResources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/resources").mock(
            return_value=httpx2.Response(200, json=_page(FILE_RESOURCE, REPO_RESOURCE, MEMORY_RESOURCE))
        )
        page = client.sessions.resources.list("session_123")
        assert_matches_type(SyncPageCursor[SessionResource], page, path=["response"])
        assert isinstance(page.data[0], SessionFileResource)
        assert isinstance(page.data[1], SessionRepositoryResource)
        assert isinstance(page.data[2], SessionMemoryStoreResource)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/resources").mock(
            return_value=httpx2.Response(200, json=_page(FILE_RESOURCE))
        )
        client.sessions.resources.list("session_123", limit=7, page="tok")
        params = _req(route).url.params
        assert params["limit"] == "7"
        assert params["page"] == "tok"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**FILE_RESOURCE, "id": "sres_789"}
        respx_mock.get("/v1/sessions/session_123/resources").mock(
            side_effect=[
                httpx2.Response(200, json=_page(FILE_RESOURCE, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [cast(Any, r).id for r in client.sessions.resources.list("session_123")]
        assert ids == ["sres_123", "sres_789"]

    @parametrize
    def test_path_params_list(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.resources.with_raw_response.list("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_add_file(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/resources").mock(
            return_value=httpx2.Response(200, json=FILE_RESOURCE)
        )
        added = client.sessions.resources.add(
            "session_123",
            resource={"type": "file", "file_id": "file_123", "mount_path": "/data", "access": "read_only"},
        )
        assert isinstance(added, SessionFileResource)
        assert json.loads(_req(route).content) == {
            "type": "file",
            "file_id": "file_123",
            "mount_path": "/data",
            "access": "read_only",
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_add_repository(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/resources").mock(
            return_value=httpx2.Response(200, json=REPO_RESOURCE)
        )
        added = client.sessions.resources.add(
            "session_123",
            resource={
                "type": "github_repository",
                "url": "https://example.test/org/repo",
                "authorization_token": "tok",
                "checkout": {"type": "commit", "sha": "abc123"},
            },
        )
        assert isinstance(added, SessionRepositoryResource)
        body = json.loads(_req(route).content)
        assert body["authorization_token"] == "tok"
        assert body["checkout"] == {"type": "commit", "sha": "abc123"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_add_memory_store(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/resources").mock(
            return_value=httpx2.Response(200, json=MEMORY_RESOURCE)
        )
        added = client.sessions.resources.add(
            "session_123", resource={"type": "memory_store", "memory_store_id": "mems_123"}
        )
        assert isinstance(added, SessionMemoryStoreResource)
        assert json.loads(_req(route).content) == {"type": "memory_store", "memory_store_id": "mems_123"}

    @parametrize
    def test_path_params_add(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.resources.with_raw_response.add(
                "", resource={"type": "memory_store", "memory_store_id": "mems_123"}
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/resources/sres_123").mock(
            return_value=httpx2.Response(200, json=FILE_RESOURCE)
        )
        retrieved = client.sessions.resources.retrieve("session_123", "sres_123")
        assert isinstance(retrieved, SessionFileResource)
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.resources.with_raw_response.retrieve("", "sres_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            client.sessions.resources.with_raw_response.retrieve("session_123", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/resources/sres_456").mock(
            return_value=httpx2.Response(200, json=REPO_RESOURCE)
        )
        client.sessions.resources.update("session_123", "sres_456", authorization_token="rotated")
        assert _req(route).method == "POST"
        assert json.loads(_req(route).content) == {"authorization_token": "rotated"}

    @parametrize
    def test_path_params_update(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            client.sessions.resources.with_raw_response.update("session_123", "", authorization_token="t")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/sessions/session_123/resources/sres_123").mock(
            return_value=httpx2.Response(200, json={"id": "sres_123", "type": "session_resource_deleted"})
        )
        deleted = client.sessions.resources.delete("session_123", "sres_123")
        assert_matches_type(DeletedSessionResource, deleted, path=["response"])
        assert _req(route).method == "DELETE"

    @parametrize
    def test_path_params_delete(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            client.sessions.resources.with_raw_response.delete("session_123", "")


class TestAsyncResources:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/resources").mock(
            return_value=httpx2.Response(200, json=_page(FILE_RESOURCE))
        )
        assert_matches_type(
            AsyncPageCursor[SessionResource],
            await async_client.sessions.resources.list("session_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_add(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/resources").mock(
            return_value=httpx2.Response(200, json=FILE_RESOURCE)
        )
        added = await async_client.sessions.resources.add(
            "session_123", resource={"type": "file", "file_id": "file_123"}
        )
        assert isinstance(added, SessionFileResource)
        assert json.loads(_req(route).content) == {"type": "file", "file_id": "file_123"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/resources/sres_123").mock(
            return_value=httpx2.Response(200, json=FILE_RESOURCE)
        )
        retrieved = await async_client.sessions.resources.retrieve("session_123", "sres_123")
        assert isinstance(retrieved, SessionFileResource)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/sessions/session_123/resources/sres_456").mock(
            return_value=httpx2.Response(200, json=REPO_RESOURCE)
        )
        await async_client.sessions.resources.update("session_123", "sres_456", authorization_token="rotated")
        assert json.loads(_req(route).content) == {"authorization_token": "rotated"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/sessions/session_123/resources/sres_123").mock(
            return_value=httpx2.Response(200, json={"id": "sres_123", "type": "session_resource_deleted"})
        )
        deleted = await async_client.sessions.resources.delete("session_123", "sres_123")
        assert_matches_type(DeletedSessionResource, deleted, path=["response"])

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.resources.with_raw_response.delete("", "sres_123")
