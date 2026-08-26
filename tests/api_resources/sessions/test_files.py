from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca
from tests.utils import assert_matches_type
from orca.pagination import SyncPage, AsyncPage
from orca.types.session_file import SessionFile, DeletedSessionFile

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

FILE: dict[str, Any] = {
    "id": "file_123",
    "type": "file",
    "filename": "notes.txt",
    "mime_type": "text/plain",
    "size_bytes": 12,
    "created_at": "2026-01-01T00:00:00Z",
    "downloadable": True,
    "scope": {"type": "session", "id": "session_123"},
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(
    *files: dict[str, Any],
    has_more: bool = False,
    first_id: str | None = None,
    last_id: str | None = None,
) -> dict[str, Any]:
    return {"data": list(files), "has_more": has_more, "first_id": first_id, "last_id": last_id}


class TestSessionFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/files").mock(return_value=httpx2.Response(200, json=_page(FILE)))
        page = client.sessions.files.list("session_123")
        assert_matches_type(SyncPage[SessionFile], page, path=["response"])
        assert [f.id for f in page.data] == ["file_123"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/files").mock(
            return_value=httpx2.Response(200, json=_page(FILE))
        )
        client.sessions.files.list("session_123", limit=5, after_id="file_000")
        params = _req(route).url.params
        assert params["limit"] == "5"
        assert params["after_id"] == "file_000"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates_forward_by_last_id(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**FILE, "id": "file_456"}
        respx_mock.get("/v1/sessions/session_123/files").mock(
            side_effect=[
                httpx2.Response(200, json=_page(FILE, has_more=True, first_id="file_123", last_id="file_123")),
                httpx2.Response(200, json=_page(second, has_more=False)),
            ]
        )
        ids = [f.id for f in client.sessions.files.list("session_123")]
        assert ids == ["file_123", "file_456"]
        assert _req(respx_mock, 1).url.params["after_id"] == "file_123"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates_backward_by_first_id(self, client: Orca, respx_mock: MockRouter) -> None:
        """A `before_id` query must keep walking backwards, not flip to `after_id`."""
        second = {**FILE, "id": "file_000"}
        respx_mock.get("/v1/sessions/session_123/files").mock(
            side_effect=[
                httpx2.Response(200, json=_page(FILE, has_more=True, first_id="file_123", last_id="file_123")),
                httpx2.Response(200, json=_page(second, has_more=False)),
            ]
        )
        ids = [f.id for f in client.sessions.files.list("session_123", before_id="file_999")]
        assert ids == ["file_123", "file_000"]
        assert _req(respx_mock, 1).url.params["before_id"] == "file_123"

    @parametrize
    def test_path_params_list(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.files.with_raw_response.list("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/files/file_123").mock(
            return_value=httpx2.Response(200, json=FILE)
        )
        file = client.sessions.files.retrieve("session_123", "file_123")
        assert file.id == "file_123"
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.files.with_raw_response.retrieve("", "file_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.sessions.files.with_raw_response.retrieve("session_123", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/files/file_123/content").mock(
            return_value=httpx2.Response(
                200, headers={"Content-Type": "application/octet-stream"}, content=b"raw-bytes"
            )
        )
        response = client.sessions.files.download("session_123", "file_123")
        assert response.content == b"raw-bytes"
        assert _req(route).headers["accept"] == "application/octet-stream"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download_accept_header_is_overridable(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/files/file_123/content").mock(
            return_value=httpx2.Response(200, content=b"raw-bytes")
        )
        client.sessions.files.download("session_123", "file_123", extra_headers={"Accept": "text/plain"})
        assert _req(route).headers["accept"] == "text/plain"

    @parametrize
    def test_path_params_download(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.files.with_raw_response.download("", "file_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.sessions.files.with_raw_response.download("session_123", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/sessions/session_123/files/file_123").mock(
            return_value=httpx2.Response(200, json={"id": "file_123", "type": "file_deleted"})
        )
        deleted = client.sessions.files.delete("session_123", "file_123")
        assert_matches_type(DeletedSessionFile, deleted, path=["response"])
        assert _req(route).method == "DELETE"

    @parametrize
    def test_path_params_delete(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.sessions.files.with_raw_response.delete("session_123", "")


class TestAsyncSessionFiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/files").mock(return_value=httpx2.Response(200, json=_page(FILE)))
        page = await async_client.sessions.files.list("session_123")
        assert_matches_type(AsyncPage[SessionFile], page, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**FILE, "id": "file_456"}
        respx_mock.get("/v1/sessions/session_123/files").mock(
            side_effect=[
                httpx2.Response(200, json=_page(FILE, has_more=True, first_id="file_123", last_id="file_123")),
                httpx2.Response(200, json=_page(second, has_more=False)),
            ]
        )
        ids = [f.id async for f in async_client.sessions.files.list("session_123")]
        assert ids == ["file_123", "file_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/session_123/files/file_123").mock(return_value=httpx2.Response(200, json=FILE))
        file = await async_client.sessions.files.retrieve("session_123", "file_123")
        assert file.id == "file_123"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/sessions/session_123/files/file_123/content").mock(
            return_value=httpx2.Response(
                200, headers={"Content-Type": "application/octet-stream"}, content=b"raw-bytes"
            )
        )
        response = await async_client.sessions.files.download("session_123", "file_123")
        assert response.content == b"raw-bytes"
        assert _req(route).headers["accept"] == "application/octet-stream"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/sessions/session_123/files/file_123").mock(
            return_value=httpx2.Response(200, json={"id": "file_123", "type": "file_deleted"})
        )
        deleted = await async_client.sessions.files.delete("session_123", "file_123")
        assert_matches_type(DeletedSessionFile, deleted, path=["response"])

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.files.with_raw_response.delete("", "file_123")
