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
from orca.types.trigger import Trigger, DeletedTrigger, TriggerKafkaSource, TriggerPulsarSource

# The resources are constructed against the client directly rather than reached
# through `client.triggers`, which is what the client mount will do once the mount
# lands in `_client.py`.
from orca.resources.triggers import Triggers, AsyncTriggers

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

CRON_SOURCE: dict[str, Any] = {
    "type": "cron",
    "schedule": "0 9 * * *",
    "timezone": "Etc/UTC",
    "payload": "Summarize.",
}

KAFKA_SOURCE: dict[str, Any] = {
    "type": "kafka",
    "connection": "conn_1",
    "topics": ["events"],
    "subscription_name": "sub-1",
    "type_class_name": "com.example.Event",
    "type_class_definition": "{}",
    "schema_type": "AVRO",
    "consumer_additional_config": {"auto.offset.reset": "earliest"},
    "input_schema_configs": {"events": {"subject": "events-value", "type": "AVRO", "version": 2}},
}

PULSAR_SOURCE: dict[str, Any] = {
    "type": "pulsar",
    "connection": "conn_2",
    "topic_pattern": "persistent://public/default/.*",
    "subscription_name": "sub-2",
}

TRIGGER: dict[str, Any] = {
    "id": "trg_123",
    "type": "trigger",
    "name": "daily-summary",
    "agent": {"type": "agent", "id": "agt_1", "version": 3},
    "session_mode": "SESSION_PER_EVENT",
    "source": CRON_SOURCE,
    "session": {
        "environment_id": "env_1",
        "title_template": None,
        "metadata": {},
        "vault_ids": [],
    },
    "replicas": 1,
    "status": "active",
    "next_fire_at": "2026-01-02T09:00:00Z",
    "last_fired_at": None,
    "error": None,
    "archived_at": None,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}

KAFKA_TRIGGER: dict[str, Any] = {
    **TRIGGER,
    "id": "trg_kafka",
    "session_mode": "SESSION_PER_KEY",
    "source": KAFKA_SOURCE,
    "replicas": 4,
}

PULSAR_TRIGGER: dict[str, Any] = {
    **TRIGGER,
    "id": "trg_pulsar",
    "session_mode": "SESSION_PER_TOPIC",
    "source": PULSAR_SOURCE,
}

DELETED_TRIGGER: dict[str, Any] = {"id": "trg_123", "type": "trigger_deleted"}

SESSION: dict[str, Any] = {"id": "ses_1", "type": "session"}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*items: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(items), "next_page": next_page}


class TestTriggers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=TRIGGER))
        trigger = Triggers(client).create(
            name="daily-summary",
            agent="agt_1",
            session_mode="SESSION_PER_EVENT",
            source={"type": "cron", "schedule": "0 9 * * *", "payload": "Summarize."},
            session={"environment_id": "env_1"},
        )
        assert_matches_type(Trigger, trigger, path=["response"])
        request = _req(route)
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "name": "daily-summary",
            "agent": "agt_1",
            "session_mode": "SESSION_PER_EVENT",
            "source": {"type": "cron", "schedule": "0 9 * * *", "payload": "Summarize."},
            "session": {"environment_id": "env_1"},
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_kafka_source_is_not_narrowed(self, client: Orca, respx_mock: MockRouter) -> None:
        """Kafka sources, every session mode, and replica counts above one all pass through."""
        route = respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=KAFKA_TRIGGER))
        trigger = Triggers(client).create(
            name="event-handler",
            agent={"type": "agent", "id": "agt_1", "version": 3},
            session_mode="SESSION_PER_KEY",
            source={
                "type": "kafka",
                "connection": "conn_1",
                "topics": ["events"],
                "subscription_name": "sub-1",
                "type_class_name": "com.example.Event",
                "type_class_definition": "{}",
                "schema_type": "AVRO",
                "consumer_additional_config": {"auto.offset.reset": "earliest"},
                "input_schema_configs": {"events": {"subject": "events-value", "type": "AVRO", "version": 2}},
            },
            session={
                "environment_id": "env_1",
                "title_template": "Event {{key}}",
                "metadata": {"team": "core"},
                "vault_ids": ["vlt_1"],
            },
            replicas=4,
            paused=True,
        )
        assert_matches_type(Trigger, trigger, path=["response"])
        assert isinstance(trigger.source, TriggerKafkaSource)
        assert trigger.source.consumer_additional_config == {"auto.offset.reset": "earliest"}
        assert trigger.replicas == 4

        body = json.loads(_req(route).content)
        assert body["session_mode"] == "SESSION_PER_KEY"
        assert body["source"] == KAFKA_SOURCE
        assert body["replicas"] == 4
        assert body["paused"] is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_pulsar_source_with_topic_pattern(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=PULSAR_TRIGGER))
        trigger = Triggers(client).create(
            name="topic-handler",
            agent="agt_1",
            session_mode="SESSION_PER_TOPIC",
            source={
                "type": "pulsar",
                "connection": "conn_2",
                "topic_pattern": "persistent://public/default/.*",
                "subscription_name": "sub-2",
            },
            session={"environment_id": "env_1"},
        )
        assert isinstance(trigger.source, TriggerPulsarSource)
        assert trigger.source.topic_pattern == "persistent://public/default/.*"
        assert json.loads(_req(route).content)["source"] == PULSAR_SOURCE

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_shared_session_mode(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/triggers").mock(
            return_value=httpx2.Response(200, json={**TRIGGER, "session_mode": "SHARED"})
        )
        Triggers(client).create(
            name="shared",
            agent="agt_1",
            session_mode="SHARED",
            source={"type": "cron", "schedule": "0 9 * * *", "timezone": "Etc/UTC", "payload": "Summarize."},
            session={"environment_id": "env_1"},
        )
        assert json.loads(_req(route).content)["session_mode"] == "SHARED"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=TRIGGER))
        response = Triggers(client).with_raw_response.create(
            name="daily-summary",
            agent="agt_1",
            session_mode="SESSION_PER_EVENT",
            source={"type": "cron", "schedule": "0 9 * * *", "payload": "Summarize."},
            session={"environment_id": "env_1"},
        )
        assert response.is_closed is True
        assert_matches_type(Trigger, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=TRIGGER))
        with Triggers(client).with_streaming_response.create(
            name="daily-summary",
            agent="agt_1",
            session_mode="SESSION_PER_EVENT",
            source={"type": "cron", "schedule": "0 9 * * *", "payload": "Summarize."},
            session={"environment_id": "env_1"},
        ) as response:
            assert not response.is_closed
            assert_matches_type(Trigger, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/triggers").mock(return_value=httpx2.Response(200, json=_page(TRIGGER)))
        assert_matches_type(SyncPageCursor[Trigger], Triggers(client).list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/triggers").mock(return_value=httpx2.Response(200, json=_page(TRIGGER)))
        Triggers(client).list(limit=20, page="tok", agent_id="agt_1")
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["page"] == "tok"
        assert params["agent_id"] == "agt_1"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**TRIGGER, "id": "trg_456"}
        respx_mock.get("/v1/triggers").mock(
            side_effect=[
                httpx2.Response(200, json=_page(TRIGGER, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [t.id for t in Triggers(client).list()] == ["trg_123", "trg_456"]
        assert _req(respx_mock, 1).url.params["page"] == "cursor-2"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/triggers/trg_123").mock(return_value=httpx2.Response(200, json=TRIGGER))
        assert_matches_type(Trigger, Triggers(client).retrieve("trg_123"), path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `trigger_id` but received ''"):
            Triggers(client).with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=TRIGGER))
        Triggers(client).retrieve("a b/c")
        assert "/v1/triggers/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/triggers/trg_123").mock(return_value=httpx2.Response(200, json=TRIGGER))
        Triggers(client).update(
            "trg_123",
            name="renamed",
            source={"type": "cron", "schedule": "0 10 * * *"},
            session={"environment_id": "env_2", "metadata": {"drop": None}},
            replicas=2,
        )
        request = _req(route)
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "name": "renamed",
            "source": {"type": "cron", "schedule": "0 10 * * *"},
            "session": {"environment_id": "env_2", "metadata": {"drop": None}},
            "replicas": 2,
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_kafka_source_patch(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/triggers/trg_kafka").mock(return_value=httpx2.Response(200, json=KAFKA_TRIGGER))
        Triggers(client).update(
            "trg_kafka",
            session_mode="SESSION_PER_TOPIC",
            source={"type": "kafka", "topics": ["events", "audit"]},
        )
        assert json.loads(_req(route).content) == {
            "session_mode": "SESSION_PER_TOPIC",
            "source": {"type": "kafka", "topics": ["events", "audit"]},
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/triggers/trg_123").mock(return_value=httpx2.Response(200, json=DELETED_TRIGGER))
        deleted = Triggers(client).delete("trg_123")
        assert_matches_type(DeletedTrigger, deleted, path=["response"])
        assert deleted.type == "trigger_deleted"
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_pause(self, client: Orca, respx_mock: MockRouter) -> None:
        paused = {**TRIGGER, "status": "paused"}
        route = respx_mock.post("/v1/triggers/trg_123/pause").mock(return_value=httpx2.Response(200, json=paused))
        trigger = Triggers(client).pause("trg_123")
        assert_matches_type(Trigger, trigger, path=["response"])
        assert trigger.status == "paused"
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_unpause(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/triggers/trg_123/unpause").mock(return_value=httpx2.Response(200, json=TRIGGER))
        trigger = Triggers(client).unpause("trg_123")
        assert_matches_type(Trigger, trigger, path=["response"])
        assert trigger.status == "active"
        assert _req(route).method == "POST"

    @parametrize
    def test_path_params_lifecycle(self, client: Orca) -> None:
        triggers = Triggers(client).with_raw_response
        for call in (triggers.delete, triggers.pause, triggers.unpause):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `trigger_id` but received ''"):
                call("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/triggers").mock(return_value=httpx2.Response(200, json=_page()))
        Triggers(client).list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"

    # ---- trigger sessions --------------------------------------------------

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_sessions_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/triggers/trg_123/sessions").mock(return_value=httpx2.Response(200, json=_page(SESSION)))
        page = Triggers(client).sessions.list("trg_123")
        assert_matches_type(SyncPageCursor[object], page, path=["response"])
        entries = cast("list[dict[str, Any]]", list(page))
        assert entries[0]["id"] == "ses_1"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_sessions_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/triggers/trg_123/sessions").mock(
            return_value=httpx2.Response(200, json=_page(SESSION))
        )
        Triggers(client).sessions.list("trg_123", limit=5, page="tok", include_archived=True)
        params = _req(route).url.params
        assert params["limit"] == "5"
        assert params["page"] == "tok"
        assert params["include_archived"] == "true"

    @parametrize
    def test_sessions_path_params(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `trigger_id` but received ''"):
            Triggers(client).sessions.with_raw_response.list("")


class TestAsyncTriggers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=TRIGGER))
        trigger = await AsyncTriggers(async_client).create(
            name="daily-summary",
            agent="agt_1",
            session_mode="SESSION_PER_EVENT",
            source={"type": "cron", "schedule": "0 9 * * *", "payload": "Summarize."},
            session={"environment_id": "env_1"},
        )
        assert_matches_type(Trigger, trigger, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create_kafka_source_is_not_narrowed(
        self, async_client: AsyncOrca, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=KAFKA_TRIGGER))
        trigger = await AsyncTriggers(async_client).create(
            name="event-handler",
            agent={"type": "agent", "id": "agt_1"},
            session_mode="SESSION_PER_KEY",
            source={"type": "kafka", "connection": "conn_1", "topics": ["events"]},
            session={"environment_id": "env_1"},
            replicas=4,
        )
        assert isinstance(trigger.source, TriggerKafkaSource)
        body = json.loads(_req(route).content)
        assert body["source"] == {"type": "kafka", "connection": "conn_1", "topics": ["events"]}
        assert body["replicas"] == 4

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=TRIGGER))
        response = await AsyncTriggers(async_client).with_raw_response.create(
            name="daily-summary",
            agent="agt_1",
            session_mode="SESSION_PER_EVENT",
            source={"type": "cron", "schedule": "0 9 * * *", "payload": "Summarize."},
            session={"environment_id": "env_1"},
        )
        assert response.is_closed is True
        assert_matches_type(Trigger, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/triggers").mock(return_value=httpx2.Response(200, json=TRIGGER))
        async with AsyncTriggers(async_client).with_streaming_response.create(
            name="daily-summary",
            agent="agt_1",
            session_mode="SESSION_PER_EVENT",
            source={"type": "cron", "schedule": "0 9 * * *", "payload": "Summarize."},
            session={"environment_id": "env_1"},
        ) as response:
            assert not response.is_closed
            assert_matches_type(Trigger, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/triggers").mock(return_value=httpx2.Response(200, json=_page(TRIGGER)))
        page = await AsyncTriggers(async_client).list(agent_id="agt_1")
        assert_matches_type(AsyncPageCursor[Trigger], page, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**TRIGGER, "id": "trg_456"}
        respx_mock.get("/v1/triggers").mock(
            side_effect=[
                httpx2.Response(200, json=_page(TRIGGER, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [t.id async for t in AsyncTriggers(async_client).list()]
        assert ids == ["trg_123", "trg_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/triggers/trg_123").mock(return_value=httpx2.Response(200, json=TRIGGER))
        trigger = await AsyncTriggers(async_client).retrieve("trg_123")
        assert_matches_type(Trigger, trigger, path=["response"])

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `trigger_id` but received ''"):
            await AsyncTriggers(async_client).with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/triggers/trg_123").mock(return_value=httpx2.Response(200, json=TRIGGER))
        await AsyncTriggers(async_client).update("trg_123", source={"type": "cron", "schedule": "0 10 * * *"})
        assert json.loads(_req(route).content) == {"source": {"type": "cron", "schedule": "0 10 * * *"}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/triggers/trg_123").mock(return_value=httpx2.Response(200, json=DELETED_TRIGGER))
        deleted = await AsyncTriggers(async_client).delete("trg_123")
        assert_matches_type(DeletedTrigger, deleted, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_pause_and_unpause(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        paused = {**TRIGGER, "status": "paused"}
        pause_route = respx_mock.post("/v1/triggers/trg_123/pause").mock(return_value=httpx2.Response(200, json=paused))
        unpause_route = respx_mock.post("/v1/triggers/trg_123/unpause").mock(
            return_value=httpx2.Response(200, json=TRIGGER)
        )
        triggers = AsyncTriggers(async_client)
        assert (await triggers.pause("trg_123")).status == "paused"
        assert (await triggers.unpause("trg_123")).status == "active"
        assert pause_route.call_count == 1
        assert unpause_route.call_count == 1

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_sessions_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/triggers/trg_123/sessions").mock(return_value=httpx2.Response(200, json=_page(SESSION)))
        page = await AsyncTriggers(async_client).sessions.list("trg_123", include_archived=False)
        assert_matches_type(AsyncPageCursor[object], page, path=["response"])

    @parametrize
    async def test_sessions_path_params(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `trigger_id` but received ''"):
            await AsyncTriggers(async_client).sessions.with_raw_response.list("")
