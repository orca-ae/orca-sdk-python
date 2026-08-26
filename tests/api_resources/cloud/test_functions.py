from __future__ import annotations

import os
import json
from typing import Any, List, cast
from email.parser import BytesParser
from email.message import Message

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.types.cloud_function_state import CloudFunctionState
from orca.types.cloud_function_stats import CloudFunctionStats, CloudFunctionInstanceStats
from orca.types.cloud_function_config import CloudFunctionConfig
from orca.types.cloud_function_status import CloudFunctionStatus, CloudFunctionInstanceStatus

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

FUNCTION_CONFIG: dict[str, Any] = {
    "tenant": "public",
    "namespace": "default",
    "name": "transform",
    "className": "com.example.Transform",
    "inputs": ["in"],
    "output": "out",
    "parallelism": 2,
    "runtime": "JAVA",
    "processingGuarantees": "ATLEAST_ONCE",
    "resources": {"cpu": 0.5, "ram": 1024, "disk": 2048},
    "inputSpecs": {"in": {"schemaType": "avro", "receiverQueueSize": 100}},
    "connection": "events",
    "snServiceAccount": "svc",
}

INSTANCE_STATS: dict[str, Any] = {
    "receivedTotal": 10,
    "processedSuccessfullyTotal": 9,
    "avgProcessLatency": 1.5,
    "1min": {"receivedTotal": 1},
    "lastInvocation": 1700000000,
    "userMetrics": {"custom": 2.0},
}

STATS: dict[str, Any] = {
    "receivedTotal": 10,
    "1min": {"receivedTotal": 1},
    "lastInvocation": 1700000000,
    "instances": [{"instanceId": 0, "metrics": {"receivedTotal": 10, "oneMin": {"receivedTotal": 1}}}],
}

INSTANCE_STATUS: dict[str, Any] = {
    "running": True,
    "numRestarts": 0,
    "latestUserExceptions": [{"exceptionString": "boom", "timestampMs": 1700000000}],
    "workerId": "worker-1",
}

STATUS: dict[str, Any] = {
    "numInstances": 2,
    "numRunning": 2,
    "instances": [{"instanceId": 0, "status": INSTANCE_STATUS}],
}

STATE: dict[str, Any] = {"key": "offset", "numberValue": 10, "version": 3}


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


class TestFunctions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        """Structured parts travel as `{field}.json` documents, not as form scalars."""
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.functions.create(
            "transform",
            data=b"jar-bytes",
            url="function://transform@latest",
            functionConfig={"parallelism": 2, "inputs": ["in"]},
        )
        request = _req(route)
        assert request.method == "POST"
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")

        parts = _parts(request)
        assert parts["url"].get_payload() == "function://transform@latest"
        assert parts["data"].get_payload(decode=True) == b"jar-bytes"

        config = parts["functionConfig"]
        assert config.get_filename() == "functionConfig.json"
        assert config.get_content_type() == "application/json"
        assert json.loads(cast(bytes, config.get_payload(decode=True))) == {"parallelism": 2, "inputs": ["in"]}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_url_only(self, client: Orca, respx_mock: MockRouter) -> None:
        """Omitted parts are dropped rather than sent empty."""
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.functions.create("transform", url="function://transform@latest")
        assert set(_parts(_req(route))) == {"url"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json=FUNCTION_CONFIG)
        )
        config = client.cloud.functions.retrieve("transform")
        assert_matches_type(CloudFunctionConfig, config, path=["response"])
        assert config.inputSpecs is not None
        assert config.inputSpecs["in"].receiverQueueSize == 100
        assert config.resources is not None
        assert config.resources.cpu == 0.5
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        """`updateOptions` carries a hyphenated wire key, aliased on the way out."""
        _gate(respx_mock, client)
        route = respx_mock.put("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.functions.update(
            "transform",
            functionConfig={"parallelism": 4},
            updateOptions={"update_auth_data": True},
        )
        request = _req(route)
        assert request.method == "PUT"
        parts = _parts(request)
        assert parts["updateOptions"].get_filename() == "updateOptions.json"
        assert json.loads(cast(bytes, parts["updateOptions"].get_payload(decode=True))) == {"update-auth-data": True}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        """The success response declares no content, so no JSON media type is requested."""
        _gate(respx_mock, client)
        route = respx_mock.delete("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.functions.delete("transform")
        request = _req(route)
        assert request.method == "DELETE"
        assert request.headers["accept"] == "*/*"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_instance_stats(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/functions/transform/0/stats").mock(
            return_value=httpx2.Response(200, json=INSTANCE_STATS)
        )
        stats = client.cloud.functions.retrieve_instance_stats("transform", "0")
        assert_matches_type(CloudFunctionInstanceStats, stats, path=["response"])
        # `1min` is not a Python identifier, so it is exposed as `one_min`.
        assert stats.one_min is not None
        assert stats.one_min.receivedTotal == 1
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/functions/transform/0/stats"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_instance_status(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions/transform/0/status").mock(
            return_value=httpx2.Response(200, json=INSTANCE_STATUS)
        )
        status = client.cloud.functions.retrieve_instance_status("transform", "0")
        assert_matches_type(CloudFunctionInstanceStatus, status, path=["response"])
        assert status.latestUserExceptions is not None
        assert status.latestUserExceptions[0].exceptionString == "boom"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_state(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/functions/transform/state/offset").mock(
            return_value=httpx2.Response(200, json=STATE)
        )
        state = client.cloud.functions.retrieve_state("transform", "offset")
        assert_matches_type(CloudFunctionState, state, path=["response"])
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/functions/transform/state/offset"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_state(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform/state/offset").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.functions.update_state("transform", "offset", state={"numberValue": 10})
        request = _req(route)
        assert request.method == "POST"
        parts = _parts(request)
        assert parts["state"].get_filename() == "state.json"
        assert parts["state"].get_content_type() == "application/json"
        assert json.loads(cast(bytes, parts["state"].get_payload(decode=True))) == {"numberValue": 10}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_stats(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions/transform/stats").mock(
            return_value=httpx2.Response(200, json=STATS)
        )
        stats = client.cloud.functions.retrieve_stats("transform")
        assert_matches_type(CloudFunctionStats, stats, path=["response"])
        assert stats.instances is not None
        assert stats.instances[0].metrics is not None
        assert stats.instances[0].metrics.oneMin is not None

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_status(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions/transform/status").mock(
            return_value=httpx2.Response(200, json=STATUS)
        )
        status = client.cloud.functions.retrieve_status("transform")
        assert_matches_type(CloudFunctionStatus, status, path=["response"])
        assert status.numRunning == 2

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/functions").mock(
            return_value=httpx2.Response(200, json=["transform", "enrich"])
        )
        names = client.cloud.functions.list()
        assert_matches_type(List[str], names, path=["response"])
        assert names == ["transform", "enrich"]
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/functions"

    @pytest.mark.parametrize(
        ("method", "suffix"),
        [("restart", ":restart"), ("start", ":start"), ("stop", ":stop")],
    )
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_lifecycle_actions(self, client: Orca, respx_mock: MockRouter, method: str, suffix: str) -> None:
        """Whole-function actions hang off the resource as a literal colon suffix."""
        _gate(respx_mock, client)
        path = f"/apis/cloud.sn.io/v1/functions/transform{suffix}"
        route = respx_mock.post(path).mock(return_value=httpx2.Response(200, json={}))
        getattr(client.cloud.functions, method)("transform")
        request = _req(route)
        assert request.method == "POST"
        assert request.url.raw_path.decode() == path
        assert "%3A" not in str(request.url)
        assert request.headers["accept"] == "*/*"

    @pytest.mark.parametrize(
        ("method", "suffix"),
        [("restart_instance", ":restart"), ("start_instance", ":start"), ("stop_instance", ":stop")],
    )
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_instance_lifecycle_actions(
        self, client: Orca, respx_mock: MockRouter, method: str, suffix: str
    ) -> None:
        """Per-instance actions put the colon after the instance segment."""
        _gate(respx_mock, client)
        path = f"/apis/cloud.sn.io/v1/functions/transform/0{suffix}"
        route = respx_mock.post(path).mock(return_value=httpx2.Response(200, json={}))
        getattr(client.cloud.functions, method)("transform", "0")
        request = _req(route)
        assert request.url.raw_path.decode() == path
        assert "%3A" not in str(request.url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_trigger(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform:trigger").mock(
            return_value=httpx2.Response(200, text="processed", headers={"content-type": "application/json"})
        )
        result = client.cloud.functions.trigger("transform", data="hello", topic="in")
        assert result == "processed"
        request = _req(route)
        assert request.url.raw_path.decode() == "/apis/cloud.sn.io/v1/functions/transform:trigger"
        parts = _parts(request)
        # `data` is declared as text here, unlike the create/update part of the same
        # name, so it stays a form scalar instead of becoming a file.
        assert parts["data"].get_filename() is None
        assert parts["data"].get_payload() == "hello"
        assert parts["topic"].get_payload() == "in"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_trigger_with_stream(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform:trigger").mock(
            return_value=httpx2.Response(200, text="ok", headers={"content-type": "application/json"})
        )
        client.cloud.functions.trigger("transform", dataStream=(b"payload"), topic="in")
        parts = _parts(_req(route))
        assert parts["dataStream"].get_payload(decode=True) == b"payload"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params(self, client: Orca, respx_mock: MockRouter) -> None:
        """The gate runs before path validation, so discovery still has to answer."""
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_name`"):
            client.cloud.functions.with_raw_response.retrieve("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `instance_id`"):
            client.cloud.functions.with_raw_response.restart_instance("transform", "")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key`"):
            client.cloud.functions.with_raw_response.retrieve_state("transform", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json=FUNCTION_CONFIG)
        )
        response = client.cloud.functions.with_raw_response.retrieve("transform")
        assert response.is_closed is True
        assert_matches_type(CloudFunctionConfig, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_stats(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions/transform/stats").mock(
            return_value=httpx2.Response(200, json=STATS)
        )
        with client.cloud.functions.with_streaming_response.retrieve_stats("transform") as response:
            assert not response.is_closed
            assert_matches_type(CloudFunctionStats, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform:restart").mock(
            return_value=httpx2.Response(200, json={})
        )
        with pytest.raises(ExtensionNotAvailableError):
            client.cloud.functions.restart("transform")
        assert route.called is False


class TestAsyncFunctions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.functions.create("transform", data=b"jar-bytes", functionConfig={"parallelism": 2})
        parts = _parts(_req(route))
        assert parts["functionConfig"].get_filename() == "functionConfig.json"
        assert parts["data"].get_payload(decode=True) == b"jar-bytes"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json=FUNCTION_CONFIG)
        )
        config = await async_client.cloud.functions.retrieve("transform")
        assert_matches_type(CloudFunctionConfig, config, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.put("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.functions.update("transform", updateOptions={"update_auth_data": False})
        parts = _parts(_req(route))
        assert json.loads(cast(bytes, parts["updateOptions"].get_payload(decode=True))) == {"update-auth-data": False}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.delete("/apis/cloud.sn.io/v1/functions/transform").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.functions.delete("transform")
        assert _req(route).headers["accept"] == "*/*"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update_state(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform/state/offset").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.functions.update_state("transform", "offset", state={"stringValue": "v"})
        parts = _parts(_req(route))
        assert parts["state"].get_filename() == "state.json"
        assert json.loads(cast(bytes, parts["state"].get_payload(decode=True))) == {"stringValue": "v"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions").mock(return_value=httpx2.Response(200, json=["transform"]))
        assert await async_client.cloud.functions.list() == ["transform"]

    @pytest.mark.parametrize(
        ("method", "path"),
        [
            ("restart", "/apis/cloud.sn.io/v1/functions/transform:restart"),
            ("start", "/apis/cloud.sn.io/v1/functions/transform:start"),
            ("stop", "/apis/cloud.sn.io/v1/functions/transform:stop"),
        ],
    )
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_lifecycle_actions(
        self, async_client: AsyncOrca, respx_mock: MockRouter, method: str, path: str
    ) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post(path).mock(return_value=httpx2.Response(200, json={}))
        await getattr(async_client.cloud.functions, method)("transform")
        assert _req(route).url.raw_path.decode() == path

    @pytest.mark.parametrize(
        ("method", "path"),
        [
            ("restart_instance", "/apis/cloud.sn.io/v1/functions/transform/0:restart"),
            ("start_instance", "/apis/cloud.sn.io/v1/functions/transform/0:start"),
            ("stop_instance", "/apis/cloud.sn.io/v1/functions/transform/0:stop"),
        ],
    )
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_instance_lifecycle_actions(
        self, async_client: AsyncOrca, respx_mock: MockRouter, method: str, path: str
    ) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post(path).mock(return_value=httpx2.Response(200, json={}))
        await getattr(async_client.cloud.functions, method)("transform", "0")
        assert _req(route).url.raw_path.decode() == path

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_trigger(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/functions/transform:trigger").mock(
            return_value=httpx2.Response(200, text="done", headers={"content-type": "application/json"})
        )
        assert await async_client.cloud.functions.trigger("transform", data="hi") == "done"
        assert _req(route).url.raw_path.decode() == "/apis/cloud.sn.io/v1/functions/transform:trigger"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_name`"):
            await async_client.cloud.functions.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve_status(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/functions/transform/status").mock(
            return_value=httpx2.Response(200, json=STATUS)
        )
        async with async_client.cloud.functions.with_streaming_response.retrieve_status("transform") as response:
            assert not response.is_closed
            assert_matches_type(CloudFunctionStatus, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get("/apis/cloud.sn.io/v1/functions").mock(return_value=httpx2.Response(200, json=[]))
        with pytest.raises(ExtensionNotAvailableError):
            await async_client.cloud.functions.list()
        assert route.called is False
