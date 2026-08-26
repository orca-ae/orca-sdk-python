from __future__ import annotations

import os
import json
from typing import Any, List, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.types.cloud_connection import CloudConnection, CloudConnectionHealth

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

CONNECTION: dict[str, Any] = {
    "name": "events",
    "spec": {
        "type": "kafka",
        "kafka": {
            "bootstrapServers": "broker:9092",
            "tls": {"enabled": True},
            "authentication": {"plainAuthConfig": {"secretName": "creds", "usernameKey": None}},
        },
    },
    "status": {"phase": "Healthy", "conditions": [{"type": "Ready", "status": "True"}]},
    "internal": False,
    "clusterRef": "cluster-1",
}

HEALTH: dict[str, Any] = {
    "name": "events",
    "phase": "Healthy",
    "healthy": True,
    "message": "ok",
    "lastTestedAt": "2026-01-01T00:00:00Z",
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


class TestConnections:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections").mock(
            return_value=httpx2.Response(200, json=[CONNECTION])
        )
        connections = client.cloud.connections.list()
        assert_matches_type(List[CloudConnection], connections, path=["response"])
        assert connections[0].spec is not None
        assert connections[0].spec.kafka is not None
        assert connections[0].spec.kafka.bootstrapServers == "broker:9092"
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/connections").mock(return_value=httpx2.Response(200, json={}))
        client.cloud.connections.create(name="events", spec={"type": "kafka"})
        request = _req(route)
        assert request.method == "POST"
        assert json.loads(request.content) == {"name": "events", "spec": {"type": "kafka"}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/connections").mock(return_value=httpx2.Response(200, json={}))
        client.cloud.connections.create(
            name="events",
            spec={
                "type": "pulsar",
                "pulsar": {
                    "serviceUrl": "pulsar://broker:6650",
                    "adminUrl": None,
                    "authentication": {"token": {"name": "secret", "key": "token"}},
                    "tls": {"enabled": True, "allowInsecureConnection": False},
                },
            },
            status={"phase": "Unknown"},
            internal=True,
            cluster_ref="cluster-1",
        )
        body = json.loads(_req(route).content)
        # camelCase reaches the wire untouched -- the cloud extension does not use
        # the snake_case spelling the core API does.
        assert body["clusterRef"] == "cluster-1"
        assert body["spec"]["pulsar"]["serviceUrl"] == "pulsar://broker:6650"
        assert body["spec"]["pulsar"]["adminUrl"] is None
        assert body["internal"] is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json=CONNECTION)
        )
        connection = client.cloud.connections.retrieve("events")
        assert_matches_type(CloudConnection, connection, path=["response"])
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/connections/events"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        """The gate runs before path validation, so discovery still has to answer."""
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.cloud.connections.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A name with a slash stays inside its own path segment."""
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections/a%2Fb").mock(
            return_value=httpx2.Response(200, json=CONNECTION)
        )
        client.cloud.connections.retrieve("a/b")
        assert _req(route).url.raw_path.decode() == "/apis/cloud.sn.io/v1/connections/a%2Fb"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.put("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.connections.update(
            "events", body_name="events", spec={"type": "other", "other": {"endpoint": "https://x"}}
        )
        request = _req(route)
        assert request.method == "PUT"
        body = json.loads(request.content)
        assert body["spec"]["other"]["endpoint"] == "https://x"
        # The path names the connection; `body_name` only fills the document's own field.
        assert body["name"] == "events"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.cloud.connections.with_raw_response.update("", spec={"type": "kafka"})

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        route = respx_mock.delete("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.connections.delete("events")
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.cloud.connections.with_raw_response.delete("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_test(self, client: Orca, respx_mock: MockRouter) -> None:
        """The action is a colon suffix on the resource, and it reaches the wire literally."""
        _gate(respx_mock, client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections/events:test").mock(
            return_value=httpx2.Response(200, json=HEALTH)
        )
        health = client.cloud.connections.test("events")
        assert_matches_type(CloudConnectionHealth, health, path=["response"])
        request = _req(route)
        assert request.method == "GET"
        assert request.url.raw_path.decode() == "/apis/cloud.sn.io/v1/connections/events:test"
        assert "%3A" not in str(request.url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_test(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.cloud.connections.with_raw_response.test("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_validate(self, client: Orca, respx_mock: MockRouter) -> None:
        """`validate` is its own path segment, not a colon action."""
        _gate(respx_mock, client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/connections/validate").mock(
            return_value=httpx2.Response(200, json={})
        )
        client.cloud.connections.validate(name="events", spec={"type": "kafka"})
        request = _req(route)
        assert request.method == "POST"
        assert request.url.path == "/apis/cloud.sn.io/v1/connections/validate"
        assert json.loads(request.content)["name"] == "events"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json=CONNECTION)
        )
        response = client.cloud.connections.with_raw_response.retrieve("events")
        assert response.is_closed is True
        assert_matches_type(CloudConnection, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json=CONNECTION)
        )
        with client.cloud.connections.with_streaming_response.retrieve("events") as response:
            assert not response.is_closed
            assert_matches_type(CloudConnection, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(self, client: Orca, respx_mock: MockRouter) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections").mock(return_value=httpx2.Response(200, json=[]))
        with pytest.raises(ExtensionNotAvailableError):
            client.cloud.connections.list()
        assert route.called is False


class TestAsyncConnections:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections").mock(
            return_value=httpx2.Response(200, json=[CONNECTION])
        )
        connections = await async_client.cloud.connections.list()
        assert_matches_type(List[CloudConnection], connections, path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/connections").mock(return_value=httpx2.Response(200, json={}))
        await async_client.cloud.connections.create(name="events", spec={"type": "kafka"}, cluster_ref="c1")
        body = json.loads(_req(route).content)
        assert body == {"name": "events", "spec": {"type": "kafka"}, "clusterRef": "c1"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json=CONNECTION)
        )
        connection = await async_client.cloud.connections.retrieve("events")
        assert_matches_type(CloudConnection, connection, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.cloud.connections.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.put("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.connections.update("events", internal=True)
        assert _req(route).method == "PUT"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.delete("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.connections.delete("events")
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_test(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections/events:test").mock(
            return_value=httpx2.Response(200, json=HEALTH)
        )
        health = await async_client.cloud.connections.test("events")
        assert_matches_type(CloudConnectionHealth, health, path=["response"])
        assert _req(route).url.raw_path.decode() == "/apis/cloud.sn.io/v1/connections/events:test"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_validate(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.post("/apis/cloud.sn.io/v1/connections/validate").mock(
            return_value=httpx2.Response(200, json={})
        )
        await async_client.cloud.connections.validate(spec={"type": "other"})
        assert _req(route).url.path == "/apis/cloud.sn.io/v1/connections/validate"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_test(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/connections/events:test").mock(
            return_value=httpx2.Response(200, json=HEALTH)
        )
        response = await async_client.cloud.connections.with_raw_response.test("events")
        assert response.is_closed is True
        assert_matches_type(CloudConnectionHealth, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/connections/events").mock(
            return_value=httpx2.Response(200, json=CONNECTION)
        )
        async with async_client.cloud.connections.with_streaming_response.retrieve("events") as response:
            assert not response.is_closed
            assert_matches_type(CloudConnection, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get("/apis/cloud.sn.io/v1/connections").mock(return_value=httpx2.Response(200, json=[]))
        with pytest.raises(ExtensionNotAvailableError):
            await async_client.cloud.connections.list()
        assert route.called is False
