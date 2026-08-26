from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.resources.cloud import Cloud, AsyncCloud
from orca.types.cloud_kafka_plugin import (
    CloudKafkaPluginInfoList,
    CloudKafkaConfigKeyInfoList,
    CloudKafkaPluginCatalogEntryList,
)
from orca.types.cloud_kafka_shared import CloudKafkaMessage, CloudKafkaServerInfo, CloudKafkaWorkerStatus
from orca.types.cloud_kafka_connector import (
    CloudKafkaTaskState,
    CloudKafkaTaskInfoList,
    CloudKafkaConnectorInfo,
    CloudKafkaConnectorOffsets,
    CloudKafkaConnectorStateInfo,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

V1 = "/apis/cloud.sn.io/v1"
KAFKA = f"{V1}/connectors/kafka"
CONNECTORS = f"{KAFKA}/connectors"
PLUGINS = f"{KAFKA}/connector-plugins"

WORKER_STATUS: dict[str, Any] = {"status": "healthy", "message": "Worker is running"}

SERVER_INFO: dict[str, Any] = {"version": "3.7.0", "commit": "abc123", "kafka_cluster_id": "cluster-1"}

# Kafka Connect serves snake_case, unlike the camelCase connector registry; both
# mirror their own wire shape.
PLUGIN_INFO: list[dict[str, Any]] = [
    {"class": "io.example.FileStreamSource", "type": "source", "version": "3.7.0"},
]

CONFIG_KEYS: list[dict[str, Any]] = [
    {
        "name": "topics",
        "type": "LIST",
        "required": True,
        "default_value": None,
        "importance": "HIGH",
        "group": "Common",
        "order_in_group": 1,
        "display_name": "Topics",
        "dependents": [],
        "order": 1,
    }
]

PLUGIN_CATALOG: list[dict[str, Any]] = [
    {
        "name": "jdbc",
        "id": "jdbc",
        "version": "1.0.0",
        "imageRepository": "example/jdbc",
        "sinkConfigFieldDefinitions": [{"fieldName": "url", "typeName": "java.lang.String"}],
    }
]

CONNECTOR_INFO: dict[str, Any] = {
    "name": "events",
    "config": {"connector.class": "io.example.FileStreamSource", "tasks.max": "2"},
    "tasks": [{"connector": "events", "task": 0}],
    "type": "source",
}

CONNECTOR_STATE_INFO: dict[str, Any] = {
    "name": "events",
    "connector": {"state": "RUNNING", "worker_id": "worker-1", "msg": "", "trace": None},
    "tasks": [{"id": 0, "state": "RUNNING", "worker_id": "worker-1", "msg": "", "trace": None}],
    "type": "source",
}

TASK_INFOS: list[dict[str, Any]] = [{"id": {"connector": "events", "task": 0}, "config": {"tasks.max": "2"}}]

TASK_STATE: dict[str, Any] = {"id": 0, "state": "RUNNING", "worker_id": "worker-1"}

OFFSETS: dict[str, Any] = {"offsets": [{"partition": {"filename": "a.txt"}, "offset": {"position": 12}}]}

MESSAGE: dict[str, Any] = {"message": "The offsets for this connector have been reset"}


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


class TestKafka:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_health(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{KAFKA}/health").mock(return_value=httpx2.Response(200, json=WORKER_STATUS))
        status = Cloud(client).connectors.kafka.health()
        assert_matches_type(CloudKafkaWorkerStatus, status, path=["response"])
        assert _req(route).method == "GET"
        assert status.status == "healthy"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_server_info(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(KAFKA).mock(return_value=httpx2.Response(200, json=SERVER_INFO))
        info = Cloud(client).connectors.kafka.server_info()
        assert_matches_type(CloudKafkaServerInfo, info, path=["response"])
        assert _req(route).method == "GET"
        assert info.kafka_cluster_id == "cluster-1"
        # The worker root is the group path itself, not a sub-resource of it.
        assert str(_req(route).url).endswith(KAFKA)


class TestKafkaPlugins:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(PLUGINS).mock(return_value=httpx2.Response(200, json=PLUGIN_INFO))
        plugins = Cloud(client).connectors.kafka.plugins.list()
        assert_matches_type(CloudKafkaPluginInfoList, plugins, path=["response"])
        assert _req(route).method == "GET"
        # `class` is a Python keyword, so the field is aliased rather than renamed.
        assert plugins[0].class_ == "io.example.FileStreamSource"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_filter(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(PLUGINS).mock(return_value=httpx2.Response(200, json=PLUGIN_INFO))
        Cloud(client).connectors.kafka.plugins.list(connectorsOnly=True)
        assert _req(route).url.params["connectorsOnly"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_config(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{PLUGINS}/FileStreamSource/config").mock(
            return_value=httpx2.Response(200, json=CONFIG_KEYS)
        )
        keys = Cloud(client).connectors.kafka.plugins.retrieve_config("FileStreamSource")
        assert_matches_type(CloudKafkaConfigKeyInfoList, keys, path=["response"])
        assert _req(route).method == "GET"
        assert keys[0].order_in_group == 1

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_catalog(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{PLUGINS}/catalog").mock(return_value=httpx2.Response(200, json=PLUGIN_CATALOG))
        catalog = Cloud(client).connectors.kafka.plugins.list_catalog()
        assert_matches_type(CloudKafkaPluginCatalogEntryList, catalog, path=["response"])
        assert _req(route).method == "GET"
        entry = catalog[0]
        assert entry.sinkConfigFieldDefinitions is not None
        assert entry.sinkConfigFieldDefinitions[0].fieldName == "url"

    @parametrize
    def test_config_validation_is_not_exposed(self, client: Orca) -> None:
        """`validateConfigs` declares only an HTTP 400 saying validation is unsupported.

        There is no successful call to make, so the SDK offers no method for it. This
        pins that absence rather than leaving it to drift back in.
        """
        plugins = Cloud(client).connectors.kafka.plugins
        assert not hasattr(plugins, "validate")
        assert not hasattr(plugins, "validate_configs")
        assert not hasattr(plugins.with_raw_response, "validate")


class TestKafkaConnectors:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(CONNECTORS).mock(return_value=httpx2.Response(200, json={"events": {}}))
        listing = Cloud(client).connectors.kafka.connectors.list()
        assert listing == {"events": {}}
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post(CONNECTORS).mock(return_value=httpx2.Response(200, json=CONNECTOR_INFO))
        info = Cloud(client).connectors.kafka.connectors.create(
            name="events",
            config={"connector.class": "io.example.FileStreamSource"},
            initial_state="PAUSED",
        )
        assert_matches_type(CloudKafkaConnectorInfo, info, path=["response"])
        request = _req(route)
        assert request.method == "POST"
        body = json.loads(request.content)
        assert body == {
            "name": "events",
            "config": {"connector.class": "io.example.FileStreamSource"},
            "initial_state": "PAUSED",
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events").mock(return_value=httpx2.Response(200, json=CONNECTOR_INFO))
        info = Cloud(client).connectors.kafka.connectors.retrieve("events")
        assert_matches_type(CloudKafkaConnectorInfo, info, path=["response"])
        assert _req(route).method == "GET"
        assert info.tasks is not None
        assert info.tasks[0].task == 0

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.delete(f"{CONNECTORS}/events").mock(return_value=httpx2.Response(200, json={}))
        Cloud(client).connectors.kafka.connectors.delete("events")
        request = _req(route)
        assert request.method == "DELETE"
        assert request.headers["accept"] == "*/*"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_config(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events/config").mock(
            return_value=httpx2.Response(200, json={"tasks.max": "2"})
        )
        config = Cloud(client).connectors.kafka.connectors.retrieve_config("events")
        assert config == {"tasks.max": "2"}
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_config(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.put(f"{CONNECTORS}/events/config").mock(
            return_value=httpx2.Response(200, json=CONNECTOR_INFO)
        )
        info = Cloud(client).connectors.kafka.connectors.update_config("events", config={"tasks.max": "3"})
        assert_matches_type(CloudKafkaConnectorInfo, info, path=["response"])
        request = _req(route)
        # A full replacement, so PUT rather than PATCH.
        assert request.method == "PUT"
        # The body is the configuration map itself, not a wrapper around it.
        assert json.loads(request.content) == {"tasks.max": "3"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_status(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events/status").mock(
            return_value=httpx2.Response(200, json=CONNECTOR_STATE_INFO)
        )
        state = Cloud(client).connectors.kafka.connectors.retrieve_status("events")
        assert_matches_type(CloudKafkaConnectorStateInfo, state, path=["response"])
        assert _req(route).method == "GET"
        assert state.connector is not None
        assert state.connector.worker_id == "worker-1"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_offsets(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events/offsets").mock(return_value=httpx2.Response(200, json=OFFSETS))
        offsets = Cloud(client).connectors.kafka.connectors.retrieve_offsets("events")
        assert_matches_type(CloudKafkaConnectorOffsets, offsets, path=["response"])
        assert _req(route).method == "GET"
        assert offsets.offsets is not None
        assert offsets.offsets[0].partition == {"filename": "a.txt"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_reset_offsets(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.delete(f"{CONNECTORS}/events/offsets").mock(return_value=httpx2.Response(200, json=MESSAGE))
        message = Cloud(client).connectors.kafka.connectors.reset_offsets("events")
        assert_matches_type(CloudKafkaMessage, message, path=["response"])
        # Resetting offsets is modelled as deleting them, not as an action endpoint.
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_offsets(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.patch(f"{CONNECTORS}/events/offsets").mock(return_value=httpx2.Response(200, json=MESSAGE))
        message = Cloud(client).connectors.kafka.connectors.update_offsets(
            "events", offsets=[{"partition": {"filename": "a.txt"}, "offset": {"position": 20}}]
        )
        assert_matches_type(CloudKafkaMessage, message, path=["response"])
        request = _req(route)
        # Only the named partitions are touched, so PATCH rather than PUT.
        assert request.method == "PATCH"
        assert json.loads(request.content) == {
            "offsets": [{"partition": {"filename": "a.txt"}, "offset": {"position": 20}}]
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_active_topics(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events/topics").mock(
            return_value=httpx2.Response(200, json={"events": {"topics": ["a"]}})
        )
        topics = Cloud(client).connectors.kafka.connectors.retrieve_active_topics("events")
        assert topics == {"events": {"topics": ["a"]}}
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_reset_active_topics(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.put(url__regex=r".*/topics.*").mock(return_value=httpx2.Response(200, json={}))
        Cloud(client).connectors.kafka.connectors.reset_active_topics("events")
        request = _req(route)
        assert request.method == "PUT"
        url = str(request.url)
        assert url.endswith(f"{CONNECTORS}/events/topics:reset")
        assert "%3A" not in url and "%3a" not in url

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_tasks(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events/tasks").mock(return_value=httpx2.Response(200, json=TASK_INFOS))
        tasks = Cloud(client).connectors.kafka.connectors.list_tasks("events")
        assert_matches_type(CloudKafkaTaskInfoList, tasks, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_task_status(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events/tasks/0/status").mock(
            return_value=httpx2.Response(200, json=TASK_STATE)
        )
        # Task 0 is a valid index, so it must not be rejected as an empty path param.
        state = Cloud(client).connectors.kafka.connectors.retrieve_task_status("events", 0)
        assert_matches_type(CloudKafkaTaskState, state, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_tasks_config(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(f"{CONNECTORS}/events/tasks-config").mock(
            return_value=httpx2.Response(200, json={"events-0": {"tasks.max": "2"}})
        )
        config = Cloud(client).connectors.kafka.connectors.retrieve_tasks_config("events")
        assert config == {"events-0": {"tasks.max": "2"}}
        assert _req(route).method == "GET"

    @pytest.mark.parametrize("action", ["pause", "resume", "stop"])
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_lifecycle_actions_use_put(self, client: Orca, respx_mock: MockRouter, action: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.put(url__regex=r".*/connectors/events.*").mock(return_value=httpx2.Response(200, json={}))
        getattr(Cloud(client).connectors.kafka.connectors, action)("events")
        request = _req(route)
        # These are PUT on this contract, not POST -- do not "normalise" them.
        assert request.method == "PUT"
        url = str(request.url)
        assert url.endswith(f"{CONNECTORS}/events:{action}")
        assert "%3A" not in url and "%3a" not in url
        assert request.headers["accept"] == "*/*"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_restart(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post(url__regex=r".*/connectors/events.*").mock(
            return_value=httpx2.Response(200, json=CONNECTOR_STATE_INFO)
        )
        Cloud(client).connectors.kafka.connectors.restart("events", includeTasks=True, onlyFailed=False)
        request = _req(route)
        # Restart is POST while pause/resume/stop are PUT; the contract mixes them.
        assert request.method == "POST"
        url = str(request.url)
        assert f"{CONNECTORS}/events:restart" in url
        assert "%3A" not in url and "%3a" not in url
        assert request.url.params["includeTasks"] == "true"
        assert request.url.params["onlyFailed"] == "false"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_restart_task(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post(f"{CONNECTORS}/events/tasks/0/restart").mock(return_value=httpx2.Response(200, json={}))
        Cloud(client).connectors.kafka.connectors.restart_task("events", 0)
        request = _req(route)
        assert request.method == "POST"
        # The task variant is a plain path segment, not a `:restart` suffix.
        assert str(request.url).endswith(f"{CONNECTORS}/events/tasks/0/restart")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get(f"{CONNECTORS}/events").mock(return_value=httpx2.Response(200, json=CONNECTOR_INFO))
        response = Cloud(client).connectors.kafka.connectors.with_raw_response.retrieve("events")
        assert response.is_closed is True
        assert_matches_type(CloudKafkaConnectorInfo, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_status(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get(f"{CONNECTORS}/events/status").mock(return_value=httpx2.Response(200, json=CONNECTOR_STATE_INFO))
        with Cloud(client).connectors.kafka.connectors.with_streaming_response.retrieve_status("events") as response:
            assert not response.is_closed
            assert_matches_type(CloudKafkaConnectorStateInfo, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        connectors = Cloud(client).connectors.kafka.connectors
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            connectors.retrieve("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            connectors.pause("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_name` but received ''"):
            Cloud(client).connectors.kafka.plugins.retrieve_config("")

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.route(url__regex=r".*connectors.*").mock(return_value=httpx2.Response(200, json={}))
        kafka = Cloud(client).connectors.kafka
        with pytest.raises(ExtensionNotAvailableError):
            kafka.health()
        with pytest.raises(ExtensionNotAvailableError):
            kafka.plugins.list()
        with pytest.raises(ExtensionNotAvailableError):
            kafka.connectors.resume("events")
        assert route.called is False


class TestAsyncKafka:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_health(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(f"{KAFKA}/health").mock(return_value=httpx2.Response(200, json=WORKER_STATUS))
        status = await AsyncCloud(async_client).connectors.kafka.health()
        assert_matches_type(CloudKafkaWorkerStatus, status, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_server_info(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(KAFKA).mock(return_value=httpx2.Response(200, json=SERVER_INFO))
        info = await AsyncCloud(async_client).connectors.kafka.server_info()
        assert_matches_type(CloudKafkaServerInfo, info, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_plugins(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        listing = respx_mock.get(PLUGINS).mock(return_value=httpx2.Response(200, json=PLUGIN_INFO))
        catalog = respx_mock.get(f"{PLUGINS}/catalog").mock(return_value=httpx2.Response(200, json=PLUGIN_CATALOG))
        config = respx_mock.get(f"{PLUGINS}/FileStreamSource/config").mock(
            return_value=httpx2.Response(200, json=CONFIG_KEYS)
        )
        plugins = AsyncCloud(async_client).connectors.kafka.plugins
        assert_matches_type(CloudKafkaPluginInfoList, await plugins.list(connectorsOnly=True), path=["response"])
        assert_matches_type(CloudKafkaPluginCatalogEntryList, await plugins.list_catalog(), path=["response"])
        assert_matches_type(
            CloudKafkaConfigKeyInfoList, await plugins.retrieve_config("FileStreamSource"), path=["response"]
        )
        assert _req(listing).url.params["connectorsOnly"] == "true"
        assert _req(catalog).method == "GET"
        assert _req(config).method == "GET"
        assert not hasattr(plugins, "validate")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post(CONNECTORS).mock(return_value=httpx2.Response(200, json=CONNECTOR_INFO))
        info = await AsyncCloud(async_client).connectors.kafka.connectors.create(
            name="events", config={"connector.class": "io.example.FileStreamSource"}
        )
        assert_matches_type(CloudKafkaConnectorInfo, info, path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update_config_uses_put(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.put(f"{CONNECTORS}/events/config").mock(
            return_value=httpx2.Response(200, json=CONNECTOR_INFO)
        )
        await AsyncCloud(async_client).connectors.kafka.connectors.update_config("events", config={"tasks.max": "3"})
        assert _req(route).method == "PUT"
        assert json.loads(_req(route).content) == {"tasks.max": "3"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_offsets_verbs(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        read = respx_mock.get(f"{CONNECTORS}/events/offsets").mock(return_value=httpx2.Response(200, json=OFFSETS))
        reset = respx_mock.delete(f"{CONNECTORS}/events/offsets").mock(return_value=httpx2.Response(200, json=MESSAGE))
        alter = respx_mock.patch(f"{CONNECTORS}/events/offsets").mock(return_value=httpx2.Response(200, json=MESSAGE))
        connectors = AsyncCloud(async_client).connectors.kafka.connectors
        await connectors.retrieve_offsets("events")
        await connectors.reset_offsets("events")
        await connectors.update_offsets("events", offsets=[{"partition": {}, "offset": {}}])
        assert _req(read).method == "GET"
        assert _req(reset).method == "DELETE"
        assert _req(alter).method == "PATCH"

    @pytest.mark.parametrize("action", ["pause", "resume", "stop"])
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_lifecycle_actions_use_put(
        self, async_client: AsyncOrca, respx_mock: MockRouter, action: str
    ) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.put(url__regex=r".*/connectors/events.*").mock(return_value=httpx2.Response(200, json={}))
        await getattr(AsyncCloud(async_client).connectors.kafka.connectors, action)("events")
        request = _req(route)
        assert request.method == "PUT"
        url = str(request.url)
        assert url.endswith(f"{CONNECTORS}/events:{action}")
        assert "%3A" not in url and "%3a" not in url

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_restart_and_tasks(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        restart = respx_mock.post(url__regex=r".*/connectors/events:restart.*").mock(
            return_value=httpx2.Response(200, json=CONNECTOR_STATE_INFO)
        )
        task = respx_mock.post(f"{CONNECTORS}/events/tasks/0/restart").mock(return_value=httpx2.Response(200, json={}))
        connectors = AsyncCloud(async_client).connectors.kafka.connectors
        await connectors.restart("events", includeTasks=True)
        await connectors.restart_task("events", 0)
        assert _req(restart).method == "POST"
        assert _req(restart).url.params["includeTasks"] == "true"
        assert _req(task).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_reset_active_topics(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.put(url__regex=r".*/topics.*").mock(return_value=httpx2.Response(200, json={}))
        await AsyncCloud(async_client).connectors.kafka.connectors.reset_active_topics("events")
        request = _req(route)
        assert request.method == "PUT"
        assert str(request.url).endswith(f"{CONNECTORS}/events/topics:reset")

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.route(url__regex=r".*connectors.*").mock(return_value=httpx2.Response(200, json={}))
        with pytest.raises(ExtensionNotAvailableError):
            await AsyncCloud(async_client).connectors.kafka.connectors.list()
        assert route.called is False
