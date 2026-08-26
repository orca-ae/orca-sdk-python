from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca
from tests.utils import assert_matches_type
from orca.pagination import SyncPage, AsyncPage
from orca.resources.files import Files, AsyncFiles
from orca.types.file_metadata import (
    DeletedFile,
    FileMetadata,
    AgentFileMetadata,
    SessionScopedFileMetadata,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

SESSION_SCOPED_FILE: dict[str, Any] = {
    "id": "file_123",
    "created_at": "2026-01-01T00:00:00Z",
    "filename": "notes.txt",
    "mime_type": "text/plain",
    "size_bytes": 5,
    "type": "file",
    "downloadable": True,
    "scope": {"type": "session", "id": "ses_1"},
}

AGENT_FILE: dict[str, Any] = {
    "id": "file_456",
    "filename": "report.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 12,
    "sha256": "a" * 64,
    "metadata": {"team": "core"},
    "purpose": "agent_output",
    "scope_id": None,
    "downloadable": True,
    "archived_at": None,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}

DELETED_FILE: dict[str, Any] = {"id": "file_123", "type": "file_deleted"}


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


def _sync(client: Orca) -> Files:
    """`Orca.files` is mounted in `_client.py`, which this change does not own;
    constructing the resource directly keeps these tests independent of that wiring
    while exercising exactly the same code path."""
    return Files(client)


def _async(client: AsyncOrca) -> AsyncFiles:
    return AsyncFiles(client)


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_upload(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        file = _sync(client).upload(file=b"hello")
        assert_matches_type(cast(Any, FileMetadata), file, path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_upload_sends_multipart_body(self, client: Orca, respx_mock: MockRouter) -> None:
        """The declared Content-Type must be multipart with an httpx-generated
        boundary, and the bytes must ride in a part named `file`."""
        route = respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        _sync(client).upload(file=("notes.txt", b"hello", "text/plain"))

        request = _req(route)
        content_type = request.headers["content-type"]
        assert content_type.startswith("multipart/form-data; boundary=")
        body = request.content
        assert b'name="file"' in body
        assert b'filename="notes.txt"' in body
        assert b"text/plain" in body
        assert b"hello" in body

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_upload_does_not_mutate_caller_input(self, client: Orca, respx_mock: MockRouter) -> None:
        """`extract_files` pops entries out of the body it is handed, so the resource
        copies first; a caller reusing its tuple must not see it emptied."""
        respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        payload = ("notes.txt", b"hello", "text/plain")
        _sync(client).upload(file=payload)
        assert payload == ("notes.txt", b"hello", "text/plain")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_upload(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        response = _sync(client).with_raw_response.upload(file=b"hello")
        assert response.is_closed is True
        assert_matches_type(cast(Any, FileMetadata), response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_upload(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        with _sync(client).with_streaming_response.upload(file=b"hello") as response:
            assert not response.is_closed
            assert_matches_type(cast(Any, FileMetadata), response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/files/file_456").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        file = _sync(client).retrieve("file_456")
        assert_matches_type(cast(Any, FileMetadata), file, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_parses_both_metadata_variants(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_123").mock(return_value=httpx2.Response(200, json=SESSION_SCOPED_FILE))
        respx_mock.get("/v1/files/file_456").mock(return_value=httpx2.Response(200, json=AGENT_FILE))

        session_scoped = _sync(client).retrieve("file_123")
        assert isinstance(session_scoped, SessionScopedFileMetadata)
        assert session_scoped.scope is not None
        assert session_scoped.scope.id == "ses_1"

        agent_file = _sync(client).retrieve("file_456")
        assert isinstance(agent_file, AgentFileMetadata)
        assert agent_file.purpose == "agent_output"
        assert agent_file.scope_id is None

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/files/file_123/content").mock(
            return_value=httpx2.Response(
                200, content=b"\x00\x01binary", headers={"content-type": "application/octet-stream"}
            )
        )
        response = _sync(client).download("file_123")
        assert isinstance(response, httpx2.Response)
        assert response.content == b"\x00\x01binary"
        assert _req(route).headers["accept"] == "application/octet-stream"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_download_accept_header_is_overridable(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/files/file_123/content").mock(
            return_value=httpx2.Response(200, content=b"x", headers={"content-type": "application/octet-stream"})
        )
        _sync(client).download("file_123", extra_headers={"Accept": "image/png"})
        assert _req(route).headers["accept"] == "image/png"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            _sync(client).with_raw_response.retrieve("")

    @parametrize
    def test_path_params_download(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            _sync(client).with_raw_response.download("")

    @parametrize
    def test_path_params_delete(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            _sync(client).with_raw_response.delete("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        _sync(client).retrieve("a b/c")
        assert "/v1/files/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files").mock(return_value=httpx2.Response(200, json=_page(AGENT_FILE)))
        assert_matches_type(SyncPage[FileMetadata], _sync(client).list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/files").mock(return_value=httpx2.Response(200, json=_page(AGENT_FILE)))
        _sync(client).list(limit=20, after_id="file_1")
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["after_id"] == "file_1"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates_forwards(self, client: Orca, respx_mock: MockRouter) -> None:
        """A forward walk follows `last_id` into the next `after_id`."""
        second = {**AGENT_FILE, "id": "file_789"}
        respx_mock.get("/v1/files").mock(
            side_effect=[
                httpx2.Response(200, json=_page(AGENT_FILE, has_more=True, first_id="file_456", last_id="file_456")),
                httpx2.Response(200, json=_page(second, has_more=False, first_id="file_789", last_id="file_789")),
            ]
        )
        ids = [f.id for f in _sync(client).list()]
        assert ids == ["file_456", "file_789"]
        assert _req(respx_mock, 1).url.params["after_id"] == "file_456"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates_backwards(self, client: Orca, respx_mock: MockRouter) -> None:
        """A `before_id` walk keeps its direction by following `first_id`."""
        second = {**AGENT_FILE, "id": "file_111"}
        respx_mock.get("/v1/files").mock(
            side_effect=[
                httpx2.Response(200, json=_page(AGENT_FILE, has_more=True, first_id="file_456", last_id="file_456")),
                httpx2.Response(200, json=_page(second, has_more=False, first_id="file_111", last_id="file_111")),
            ]
        )
        ids = [f.id for f in _sync(client).list(before_id="file_999")]
        assert ids == ["file_456", "file_111"]
        second_params = _req(respx_mock, 1).url.params
        assert second_params["before_id"] == "file_456"
        assert second_params.get("after_id") is None

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_stops_when_has_more_is_false(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/files").mock(
            return_value=httpx2.Response(200, json=_page(AGENT_FILE, has_more=False, last_id="file_456"))
        )
        assert [f.id for f in _sync(client).list()] == ["file_456"]
        assert route.call_count == 1

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/files/file_123").mock(return_value=httpx2.Response(200, json=DELETED_FILE))
        deleted = _sync(client).delete("file_123")
        assert_matches_type(DeletedFile, deleted, path=["response"])
        assert deleted.type == "file_deleted"
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/files").mock(return_value=httpx2.Response(200, json=_page()))
        _sync(client).list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_upload(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        file = await _async(async_client).upload(file=("notes.txt", b"hello", "text/plain"))
        assert_matches_type(cast(Any, FileMetadata), file, path=["response"])
        request = _req(route)
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        assert b'name="file"' in request.content

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_upload(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        response = await _async(async_client).with_raw_response.upload(file=b"hello")
        assert response.is_closed is True
        assert_matches_type(cast(Any, FileMetadata), await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_upload(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/files").mock(return_value=httpx2.Response(200, json=AGENT_FILE))
        async with _async(async_client).with_streaming_response.upload(file=b"hello") as response:
            assert not response.is_closed
            assert_matches_type(cast(Any, FileMetadata), await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_123").mock(return_value=httpx2.Response(200, json=SESSION_SCOPED_FILE))
        file = await _async(async_client).retrieve("file_123")
        assert isinstance(file, SessionScopedFileMetadata)

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await _async(async_client).with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/files/file_123/content").mock(
            return_value=httpx2.Response(
                200, content=b"\x00\x01binary", headers={"content-type": "application/octet-stream"}
            )
        )
        response = await _async(async_client).download("file_123")
        assert isinstance(response, httpx2.Response)
        assert response.content == b"\x00\x01binary"
        assert _req(route).headers["accept"] == "application/octet-stream"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files").mock(return_value=httpx2.Response(200, json=_page(AGENT_FILE)))
        assert_matches_type(AsyncPage[FileMetadata], await _async(async_client).list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates_forwards(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**AGENT_FILE, "id": "file_789"}
        respx_mock.get("/v1/files").mock(
            side_effect=[
                httpx2.Response(200, json=_page(AGENT_FILE, has_more=True, first_id="file_456", last_id="file_456")),
                httpx2.Response(200, json=_page(second, has_more=False, first_id="file_789", last_id="file_789")),
            ]
        )
        ids = [f.id async for f in _async(async_client).list()]
        assert ids == ["file_456", "file_789"]
        assert _req(respx_mock, 1).url.params["after_id"] == "file_456"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/files/file_123").mock(return_value=httpx2.Response(200, json=DELETED_FILE))
        assert_matches_type(DeletedFile, await _async(async_client).delete("file_123"), path=["response"])
