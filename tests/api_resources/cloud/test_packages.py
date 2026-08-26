from __future__ import annotations

import os
import json
from typing import Any, cast
from email.parser import BytesParser
from email.message import Message

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

METADATA: dict[str, Any] = {
    "description": "Transform",
    "contact": "team@example.test",
    "createTime": 1700000000000,
    "modificationTime": 1700000001000,
    "properties": {"owner": "core"},
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _gate(respx_mock: MockRouter, client: Orca | AsyncOrca, *, available: bool = True) -> Any:
    """Stub `GET /apis` and drop any discovery result the client already cached.

    Discovery is cached per base URL and the client fixture is session-scoped, so
    without the reset whichever cloud test ran first would decide the answer for
    every test after it.
    """
    client._extension_groups.clear()
    groups = [{"name": "cloud.sn.io"}] if available else []
    return respx_mock.get("/apis").mock(
        return_value=httpx2.Response(200, json={"kind": "APIGroupList", "groups": groups})
    )


def _parts(request: httpx2.Request) -> dict[str, Message]:
    """Decode a multipart request body into `{field name: part}`.

    Reusing the stdlib MIME parser keeps the assertions about filenames and part
    content types honest -- they read what actually went on the wire rather than
    what the encoder intended.
    """
    content_type = request.headers["content-type"]
    raw = b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + request.content
    parsed = BytesParser().parsebytes(raw)
    parts: dict[str, Message] = {}
    for part in parsed.get_payload():
        assert isinstance(part, Message)
        name = part.get_param("name", header="content-disposition")
        assert isinstance(name, str)
        parts[name] = part
    return parts


class TestPackages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        """The contract declares no schema here, so the parsed body comes back as-is."""
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function").mock(
            return_value=httpx2.Response(200, json=["function://public/default/transform"])
        )
        packages = client.cloud.packages.list("function")
        assert packages == ["function://public/default/transform"]
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_versions(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform").mock(
            return_value=httpx2.Response(200, json=["v1", "v2"])
        )
        assert client.cloud.packages.list_versions("function", "transform") == ["v1", "v2"]
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/packages/function/transform"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Orca, respx_mock: MockRouter) -> None:
        """Downloads serve bytes, so the raw HTTP response is handed back."""
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform/v1").mock(
            return_value=httpx2.Response(200, content=b"archive-bytes")
        )
        response = client.cloud.packages.download("function", "transform", "v1")
        assert isinstance(response, httpx2.Response)
        assert response.content == b"archive-bytes"
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/packages/function/transform/v1"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_upload(self, client: Orca, respx_mock: MockRouter) -> None:
        """`metadata` is structured, so it travels as its own JSON part."""
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/packages/function/transform/v1").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.packages.upload(
            "function",
            "transform",
            "v1",
            metadata={"description": "Transform", "properties": {"owner": "core"}},
            file=b"archive-bytes",
        )
        request = _req(route)
        assert request.method == "POST"
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")

        parts = _parts(request)
        assert parts["file"].get_payload(decode=True) == b"archive-bytes"
        assert parts["metadata"].get_filename() == "metadata.json"
        assert parts["metadata"].get_content_type() == "application/json"
        assert json.loads(cast(bytes, parts["metadata"].get_payload(decode=True))) == {
            "description": "Transform",
            "properties": {"owner": "core"},
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_upload_file_only(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/packages/function/transform/v1").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.packages.upload(
            "function", "transform", "v1", file=("t.jar", b"bytes", "application/java-archive")
        )
        parts = _parts(_req(route))
        assert set(parts) == {"file"}
        assert parts["file"].get_filename() == "t.jar"
        assert parts["file"].get_content_type() == "application/java-archive"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.delete("/apis/cloud.sn.io/v1/packages/function/transform/v1").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.packages.delete("function", "transform", "v1")
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_metadata(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata").mock(
            return_value=httpx2.Response(200, json=METADATA)
        )
        assert client.cloud.packages.retrieve_metadata("function", "transform", "v1") == METADATA
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_metadata(self, client: Orca, respx_mock: MockRouter) -> None:
        """Metadata replacement is JSON, not multipart, and it is a PUT."""
        _gate(respx_mock, client)
        route = respx_mock.put("/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.packages.update_metadata(
            "function",
            "transform",
            "v1",
            description="Transform",
            contact="team@example.test",
            create_time=1700000000000,
            modification_time=1700000001000,
            properties={"owner": "core"},
        )
        request = _req(route)
        assert request.method == "PUT"
        assert request.headers["content-type"] == "application/json"
        assert json.loads(request.content) == METADATA

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params(self, client: Orca, respx_mock: MockRouter) -> None:
        """The gate runs before path validation, so discovery still has to answer."""
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `type`"):
            client.cloud.packages.with_raw_response.list("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `package_name`"):
            client.cloud.packages.with_raw_response.list_versions("function", "")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version`"):
            client.cloud.packages.with_raw_response.download("function", "transform", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A package name with a slash stays inside its own path segment."""
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function/a%2Fb").mock(
            return_value=httpx2.Response(200, json=[])
        )
        client.cloud.packages.list_versions("function", "a/b")
        assert _req(route).url.raw_path.decode() == "/apis/cloud.sn.io/v1/packages/function/a%2Fb"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve_metadata(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata").mock(
            return_value=httpx2.Response(200, json=METADATA)
        )
        response = client.cloud.packages.with_raw_response.retrieve_metadata("function", "transform", "v1")
        assert response.is_closed is True
        assert response.parse() == METADATA

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_metadata(self, client: Orca, respx_mock: MockRouter) -> None:
        """Streaming wrappers are exercised on a parsed method.

        `download` casts to the raw `httpx2.Response`, and the streaming wrapper
        hands back a response the caller must drain itself; `test_method_download`
        covers that path directly instead.
        """
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata").mock(
            return_value=httpx2.Response(200, json=METADATA)
        )
        with client.cloud.packages.with_streaming_response.retrieve_metadata("function", "transform", "v1") as response:
            assert not response.is_closed
            assert response.parse() == METADATA
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function").mock(
            return_value=httpx2.Response(200, json=[])
        )
        with pytest.raises(ExtensionNotAvailableError):
            client.cloud.packages.list("function")
        assert route.called is False


class TestAsyncPackages:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function").mock(
            return_value=httpx2.Response(200, json=["function://public/default/transform"])
        )
        assert await async_client.cloud.packages.list("function") == ["function://public/default/transform"]
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list_versions(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform").mock(
            return_value=httpx2.Response(200, json=["v1"])
        )
        assert await async_client.cloud.packages.list_versions("function", "transform") == ["v1"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform/v1").mock(
            return_value=httpx2.Response(200, content=b"archive-bytes")
        )
        response = await async_client.cloud.packages.download("function", "transform", "v1")
        assert isinstance(response, httpx2.Response)
        assert response.content == b"archive-bytes"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_upload(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/packages/function/transform/v1").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.packages.upload(
            "function", "transform", "v1", metadata={"contact": "team@example.test"}, file=b"bytes"
        )
        parts = _parts(_req(route))
        assert parts["metadata"].get_filename() == "metadata.json"
        assert json.loads(cast(bytes, parts["metadata"].get_payload(decode=True))) == {"contact": "team@example.test"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.delete("/apis/cloud.sn.io/v1/packages/function/transform/v1").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.packages.delete("function", "transform", "v1")
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve_metadata(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata").mock(
            return_value=httpx2.Response(200, json=METADATA)
        )
        assert await async_client.cloud.packages.retrieve_metadata("function", "transform", "v1") == METADATA

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update_metadata(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.put("/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.packages.update_metadata("function", "transform", "v1", description="Transform")
        request = _req(route)
        assert request.method == "PUT"
        assert json.loads(request.content) == {"description": "Transform"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `type`"):
            await async_client.cloud.packages.with_raw_response.list("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve_metadata(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/packages/function/transform/v1/metadata").mock(
            return_value=httpx2.Response(200, json=METADATA)
        )
        async with async_client.cloud.packages.with_streaming_response.retrieve_metadata(
            "function", "transform", "v1"
        ) as response:
            assert not response.is_closed
            assert await response.parse() == METADATA
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get("/apis/cloud.sn.io/v1/packages/function").mock(
            return_value=httpx2.Response(200, json=[])
        )
        with pytest.raises(ExtensionNotAvailableError):
            await async_client.cloud.packages.list("function")
        assert route.called is False
