from __future__ import annotations

import os
import re
from typing import Any, Union, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.resources.cloud import Cloud, AsyncCloud
from orca.resources.cloud.connectors import SinkConnectors, SourceConnectors, AsyncSinkConnectors, AsyncSourceConnectors
from orca.types.cloud_connector_sink import (
    CloudSinkConfig,
    CloudSinkStatus,
    CloudSinkNameList,
    CloudSinkInstanceStatus,
)
from orca.types.cloud_connector_source import (
    CloudSourceConfig,
    CloudSourceStatus,
    CloudSourceNameList,
    CloudSourceInstanceStatus,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

V1 = "/apis/cloud.sn.io/v1"

# camelCase because the connector registry serves these fields that way; the SDK
# mirrors the wire shape rather than renaming it.
SINK_CONFIG: dict[str, Any] = {
    "tenant": "public",
    "namespace": "default",
    "name": "archive",
    "className": "io.example.ArchiveSink",
    "inputs": ["events"],
    "parallelism": 2,
    "processingGuarantees": "ATLEAST_ONCE",
    "resources": {"cpu": 0.5, "ram": 1024, "disk": 2048},
    "inputSpecs": {"events": {"schemaType": "avro", "receiverQueueSize": 100}},
    "connection": "primary",
}

SOURCE_CONFIG: dict[str, Any] = {
    "tenant": "public",
    "namespace": "default",
    "name": "events",
    "className": "io.example.EventSource",
    "topicName": "events",
    "producerConfig": {"maxPendingMessages": 10, "compressionType": "ZSTD"},
    "batchSourceConfig": {"discoveryTriggererClassName": "io.example.Cron"},
    "connection": "primary",
}

SINK_STATUS: dict[str, Any] = {
    "numInstances": 1,
    "numRunning": 1,
    "instances": [{"instanceId": 0, "status": {"running": True, "numWrittenToSink": 7}}],
}

SOURCE_STATUS: dict[str, Any] = {
    "numInstances": 1,
    "numRunning": 1,
    "instances": [{"instanceId": 0, "status": {"running": True, "numWritten": 7}}],
}

SINK_INSTANCE_STATUS: dict[str, Any] = {
    "running": True,
    "numRestarts": 1,
    "numReadFromPulsar": 12,
    "latestSinkExceptions": [{"exceptionString": "boom", "timestampMs": 1}],
    "workerId": "worker-1",
}

SOURCE_INSTANCE_STATUS: dict[str, Any] = {
    "running": True,
    "numRestarts": 1,
    "numReceivedFromSource": 12,
    "workerId": "worker-1",
}

# Sinks and sources are the same 13-method surface under different segments, so
# every shared assertion runs against both.
KINDS = pytest.mark.parametrize("kind", ["sinks", "sources"])

CONFIGS = {"sinks": SINK_CONFIG, "sources": SOURCE_CONFIG}
STATUSES = {"sinks": SINK_STATUS, "sources": SOURCE_STATUS}
INSTANCE_STATUSES = {"sinks": SINK_INSTANCE_STATUS, "sources": SOURCE_INSTANCE_STATUS}

# (method name, path suffix) for the endpoints whose action is a `:verb` suffix.
ALL_ACTIONS = [("restart", ":restart"), ("start", ":start"), ("stop", ":stop")]
INSTANCE_ACTIONS = [("restart_instance", ":restart"), ("start_instance", ":start"), ("stop_instance", ":stop")]

SyncKind = Union[SinkConnectors, SourceConnectors]
AsyncKind = Union[AsyncSinkConnectors, AsyncSourceConnectors]


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


def _sync_kind(client: Orca, kind: str) -> SyncKind:
    """Resolve a segment name to its resource through the real router chain."""
    connectors = Cloud(client).connectors
    return connectors.sinks if kind == "sinks" else connectors.sources


def _async_kind(client: AsyncOrca, kind: str) -> AsyncKind:
    connectors = AsyncCloud(client).connectors
    return connectors.sinks if kind == "sinks" else connectors.sources


def _config_type(kind: str) -> Any:
    return CloudSinkConfig if kind == "sinks" else CloudSourceConfig


def _status_type(kind: str) -> Any:
    return CloudSinkStatus if kind == "sinks" else CloudSourceStatus


def _instance_status_type(kind: str) -> Any:
    return CloudSinkInstanceStatus if kind == "sinks" else CloudSourceInstanceStatus


def _name_list_type(kind: str) -> Any:
    return CloudSinkNameList if kind == "sinks" else CloudSourceNameList


def _config_kwarg(kind: str, value: Any) -> dict[str, Any]:
    """The config argument is named after its own connector kind."""
    return {"sink_config" if kind == "sinks" else "source_config": value}


class TestConnectors:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{V1}/connectors/{kind}").mock(
            return_value=httpx2.Response(200, json=["archive", "audit"])
        )
        names = _sync_kind(client, kind).list()
        assert_matches_type(_name_list_type(kind), names, path=["response"])
        assert names == ["archive", "audit"]
        assert _req(route).method == "GET"

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{V1}/connectors/{kind}/archive").mock(
            return_value=httpx2.Response(200, json=CONFIGS[kind])
        )
        got = _sync_kind(client, kind).retrieve("archive")
        assert_matches_type(_config_type(kind), got, path=["response"])
        assert _req(route).method == "GET"
        assert got.className == CONFIGS[kind]["className"]
        assert got.connection == "primary"

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        _sync_kind(client, kind).create(
            "archive",
            url="https://packages.test/archive.nar",
            **_config_kwarg(kind, CONFIGS[kind]),
        )
        request = _req(route)
        assert request.method == "POST"
        assert request.headers["content-type"].startswith("multipart/form-data")
        part = "sinkConfig" if kind == "sinks" else "sourceConfig"
        # The structured part travels as its own JSON document, not as form scalars.
        assert f'filename="{part}.json"'.encode() in request.content
        assert b"application/json" in request.content
        assert b"https://packages.test/archive.nar" in request.content

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.put(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        _sync_kind(client, kind).update(
            "archive",
            update_options={"update_auth_data": True},
            **_config_kwarg(kind, CONFIGS[kind]),
        )
        request = _req(route)
        assert request.method == "PUT"
        assert b'filename="updateOptions.json"' in request.content
        # The wire name is hyphenated, so the aliased field must be renamed on the way out.
        assert b"update-auth-data" in request.content
        assert b"update_auth_data" not in request.content

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_file(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        _sync_kind(client, kind).create("archive", data=b"connector-bytes")
        assert b"connector-bytes" in _req(route).content

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_multipart_part_names_are_wire_names(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        """Every part is named with the wire key, including the file part.

        The file part's name comes from whatever key reaches the encoder, so splitting
        the arguments out before the transform would name it after the Python argument
        instead. That failure is silent -- the server rejects the part, but no type
        checker, linter, or round-trip assertion sees it -- so the names are pinned here.
        """
        _gate(respx_mock, client)
        route = respx_mock.post(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        _sync_kind(client, kind).create(
            "archive",
            data=b"connector-bytes",
            url="https://packages.test/archive.nar",
            **_config_kwarg(kind, CONFIGS[kind]),
        )
        # `(?<!file)` matters: `filename="..."` contains `name="..."` as a substring.
        names = set(re.findall(r'(?<!file)name="([^"]+)"', _req(route).content.decode("utf-8", "replace")))
        assert names == {"data", "url", "sinkConfig" if kind == "sinks" else "sourceConfig"}

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.delete(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        _sync_kind(client, kind).delete("archive")
        request = _req(route)
        assert request.method == "DELETE"
        # No modelled success body, so the request does not insist on JSON back.
        assert request.headers["accept"] == "*/*"

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_status(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{V1}/connectors/{kind}/archive/status").mock(
            return_value=httpx2.Response(200, json=STATUSES[kind])
        )
        got = _sync_kind(client, kind).retrieve_status("archive")
        assert_matches_type(_status_type(kind), got, path=["response"])
        assert _req(route).method == "GET"
        assert got.numRunning == 1

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_instance_status(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{V1}/connectors/{kind}/archive/0/status").mock(
            return_value=httpx2.Response(200, json=INSTANCE_STATUSES[kind])
        )
        got = _sync_kind(client, kind).retrieve_instance_status("archive", "0")
        assert_matches_type(_instance_status_type(kind), got, path=["response"])
        assert _req(route).method == "GET"
        assert got.running is True

    @pytest.mark.parametrize(("method", "suffix"), ALL_ACTIONS)
    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_action_all_instances(
        self,
        client: Orca,
        respx_mock: MockRouter,
        kind: str,
        method: str,
        suffix: str,
    ) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post(url__regex=rf".*/connectors/{kind}/.*").mock(return_value=httpx2.Response(200, json={}))
        getattr(_sync_kind(client, kind), method)("archive")
        request = _req(route)
        assert request.method == "POST"
        url = str(request.url)
        # The colon is part of the route, not an escape: it must survive verbatim.
        assert url.endswith(f"{V1}/connectors/{kind}/archive{suffix}")
        assert "%3A" not in url and "%3a" not in url
        assert request.headers["accept"] == "*/*"

    @pytest.mark.parametrize(("method", "suffix"), INSTANCE_ACTIONS)
    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_action_one_instance(
        self,
        client: Orca,
        respx_mock: MockRouter,
        kind: str,
        method: str,
        suffix: str,
    ) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post(url__regex=rf".*/connectors/{kind}/.*").mock(return_value=httpx2.Response(200, json={}))
        getattr(_sync_kind(client, kind), method)("archive", "0")
        request = _req(route)
        assert request.method == "POST"
        url = str(request.url)
        assert url.endswith(f"{V1}/connectors/{kind}/archive/0{suffix}")
        assert "%3A" not in url and "%3a" not in url

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get(f"{V1}/connectors/sinks/archive").mock(return_value=httpx2.Response(200, json=SINK_CONFIG))
        response = Cloud(client).connectors.sinks.with_raw_response.retrieve("archive")
        assert response.is_closed is True
        assert_matches_type(CloudSinkConfig, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get(f"{V1}/connectors/sources/events").mock(return_value=httpx2.Response(200, json=SOURCE_CONFIG))
        with Cloud(client).connectors.sources.with_streaming_response.retrieve("events") as response:
            assert not response.is_closed
            assert_matches_type(CloudSourceConfig, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params(self, client: Orca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, client)
        resource = _sync_kind(client, kind)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            resource.retrieve("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `instance_id` but received ''"):
            resource.restart_instance("archive", "")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        _gate(respx_mock, client)
        route = respx_mock.get(url__regex=r".*connectors.*").mock(return_value=httpx2.Response(200, json=SINK_CONFIG))
        Cloud(client).connectors.sinks.retrieve("a b/c")
        assert f"{V1}/connectors/sinks/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.route(url__regex=r".*connectors.*").mock(return_value=httpx2.Response(200, json={}))
        with pytest.raises(ExtensionNotAvailableError):
            Cloud(client).connectors.sinks.list()
        with pytest.raises(ExtensionNotAvailableError):
            Cloud(client).connectors.sources.stop("archive")
        assert route.called is False


class TestAsyncConnectors:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(f"{V1}/connectors/{kind}").mock(
            return_value=httpx2.Response(200, json=["archive", "audit"])
        )
        names = await _async_kind(async_client, kind).list()
        assert_matches_type(_name_list_type(kind), names, path=["response"])
        assert _req(route).method == "GET"

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(f"{V1}/connectors/{kind}/archive").mock(
            return_value=httpx2.Response(200, json=CONFIGS[kind])
        )
        got = await _async_kind(async_client, kind).retrieve("archive")
        assert_matches_type(_config_type(kind), got, path=["response"])
        assert _req(route).method == "GET"

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        await _async_kind(async_client, kind).create("archive", **_config_kwarg(kind, CONFIGS[kind]))
        request = _req(route)
        assert request.method == "POST"
        part = "sinkConfig" if kind == "sinks" else "sourceConfig"
        assert f'filename="{part}.json"'.encode() in request.content

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.put(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        await _async_kind(async_client, kind).update("archive", **_config_kwarg(kind, CONFIGS[kind]))
        assert _req(route).method == "PUT"

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.delete(f"{V1}/connectors/{kind}/archive").mock(return_value=httpx2.Response(200, json={}))
        await _async_kind(async_client, kind).delete("archive")
        assert _req(route).method == "DELETE"

    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_statuses(self, async_client: AsyncOrca, respx_mock: MockRouter, kind: str) -> None:
        _gate(respx_mock, async_client)
        aggregate = respx_mock.get(f"{V1}/connectors/{kind}/archive/status").mock(
            return_value=httpx2.Response(200, json=STATUSES[kind])
        )
        instance = respx_mock.get(f"{V1}/connectors/{kind}/archive/0/status").mock(
            return_value=httpx2.Response(200, json=INSTANCE_STATUSES[kind])
        )
        resource = _async_kind(async_client, kind)
        assert_matches_type(_status_type(kind), await resource.retrieve_status("archive"), path=["response"])
        assert_matches_type(
            _instance_status_type(kind),
            await resource.retrieve_instance_status("archive", "0"),
            path=["response"],
        )
        assert _req(aggregate).method == "GET"
        assert _req(instance).method == "GET"

    @pytest.mark.parametrize(("method", "suffix"), ALL_ACTIONS)
    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_action_all_instances(
        self,
        async_client: AsyncOrca,
        respx_mock: MockRouter,
        kind: str,
        method: str,
        suffix: str,
    ) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post(url__regex=rf".*/connectors/{kind}/.*").mock(return_value=httpx2.Response(200, json={}))
        await getattr(_async_kind(async_client, kind), method)("archive")
        url = str(_req(route).url)
        assert url.endswith(f"{V1}/connectors/{kind}/archive{suffix}")
        assert "%3A" not in url and "%3a" not in url

    @pytest.mark.parametrize(("method", "suffix"), INSTANCE_ACTIONS)
    @KINDS
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_action_one_instance(
        self,
        async_client: AsyncOrca,
        respx_mock: MockRouter,
        kind: str,
        method: str,
        suffix: str,
    ) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post(url__regex=rf".*/connectors/{kind}/.*").mock(return_value=httpx2.Response(200, json={}))
        await getattr(_async_kind(async_client, kind), method)("archive", "0")
        url = str(_req(route).url)
        assert url.endswith(f"{V1}/connectors/{kind}/archive/0{suffix}")
        assert "%3A" not in url and "%3a" not in url

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get(f"{V1}/connectors/sinks").mock(return_value=httpx2.Response(200, json=["archive"]))
        response = await AsyncCloud(async_client).connectors.sinks.with_raw_response.list()
        assert response.is_closed is True
        assert_matches_type(CloudSinkNameList, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.route(url__regex=r".*connectors.*").mock(return_value=httpx2.Response(200, json={}))
        with pytest.raises(ExtensionNotAvailableError):
            await AsyncCloud(async_client).connectors.sinks.list()
        assert route.called is False
