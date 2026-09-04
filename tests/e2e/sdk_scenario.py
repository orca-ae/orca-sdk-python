"""Exercise the public SDK against either supported E2E topology."""

from __future__ import annotations

import os
import sys
import time
from typing import Any
from collections.abc import Callable

from orca import Orca, PermissionDeniedError, ExtensionNotAvailableError

BETA_HEADERS = {"orca-beta": "managed-agents-2026-04-01"}
PROVIDER = "anthropic"  # wire-value
MODEL_ID = "claude-sonnet-4-5-20250929"  # wire-value


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


workspace_api_key = os.environ.get("ORCA_E2E_API_KEY")
access_token = os.environ.get("ORCA_E2E_ACCESS_TOKEN")
if bool(workspace_api_key) == bool(access_token):
    raise RuntimeError("exactly one of ORCA_E2E_API_KEY or ORCA_E2E_ACCESS_TOKEN is required")

client = Orca(
    api_key=access_token,
    base_url=required_env("ORCA_BASE_URL"),
    default_headers={"x-api-key": workspace_api_key} if workspace_api_key else None,
    max_retries=0,
)
expect_cloud = os.environ.get("ORCA_E2E_EXPECT_CLOUD") == "true"
expect_execution = os.environ.get("ORCA_E2E_EXPECT_EXECUTION") == "true"
run_suffix = "-".join(
    [os.environ.get("GITHUB_RUN_ID", "local"), os.environ.get("GITHUB_RUN_ATTEMPT", "0"), str(os.getpid())]
)
resource_prefix = f"sdk-e2e-{run_suffix}"
resources: dict[str, Any] = {}
failures: list[str] = []


def run_scenario(name: str, operation: Callable[[], None]) -> None:
    print(f"[RUN] {name}", flush=True)
    try:
        operation()
    except Exception as error:  # noqa: BLE001 - collect all E2E evidence before cleanup
        failures.append(f"{name}: {error!r}")
        print(f"[FAIL] {name}: {error!r}", file=sys.stderr, flush=True)
    else:
        print(f"[PASS] {name}", flush=True)


def cleanup_resources(strict: bool) -> None:
    cleanup_failures: list[str] = []

    def cleanup(name: str, operation: Callable[[], object]) -> bool:
        try:
            operation()
        except Exception as error:  # noqa: BLE001 - best-effort cleanup
            cleanup_failures.append(f"{name}: {error!r}")
            return False
        return True

    trigger = resources.get("trigger")
    if trigger is not None:
        if cleanup("delete trigger", lambda: client.triggers.delete(trigger.id)):
            resources.pop("trigger", None)

    session = resources.get("session")
    if session is not None:
        if cleanup("archive session", lambda: client.sessions.archive(session.id)):
            resources.pop("session", None)

    agent = resources.get("agent")
    guardrail = resources.get("guardrail")
    if agent is not None:
        if guardrail is not None:
            cleanup(
                "clear agent guardrails",
                lambda: client.agents.update(agent.id, guardrail_ids=None, extra_headers=BETA_HEADERS),
            )
        if cleanup("archive agent", lambda: client.agents.archive(agent.id)):
            resources.pop("agent", None)

    if guardrail is not None:
        cleanup("archive guardrail", lambda: client.guardrails.archive(guardrail.id))
        if cleanup("delete guardrail", lambda: client.guardrails.delete(guardrail.id)):
            resources.pop("guardrail", None)

    environment = resources.get("environment")
    if environment is not None:
        if cleanup("archive environment", lambda: client.environments.archive(environment.id)):
            resources.pop("environment", None)

    file = resources.get("file")
    if file is not None:
        if cleanup("delete file", lambda: client.files.delete(file.id)):
            resources.pop("file", None)

    if cleanup_failures:
        if strict:
            raise RuntimeError("; ".join(cleanup_failures))
        for failure in cleanup_failures:
            print(f"[CLEANUP FAIL] {failure}", file=sys.stderr)


def check_discovery() -> None:
    discovery = client.discovery.groups()
    assert discovery.kind == "APIGroupList"
    has_cloud = any(group.name == "cloud.sn.io" for group in discovery.groups)
    assert has_cloud is expect_cloud
    if expect_cloud:
        api_resources = client.cloud.api_resources.list()
        assert api_resources.group_version == "cloud.sn.io/v1"
        assert api_resources.resources
        return

    try:
        client.cloud.api_resources.list()
    except ExtensionNotAvailableError as error:
        assert error.group == "cloud.sn.io"
    else:
        raise AssertionError("cloud call was not gated")

    policy = client.discovery.policy_group_resources()
    pricing = client.discovery.pricing_group_resources()
    assert any(resource.name == "guardrails" for resource in policy.resources)
    assert any(resource.name == "modelprices" for resource in pricing.resources)


def check_policy_and_pricing() -> None:
    types = client.guardrails.list_types()
    assert any(item.name == "block_tools" for item in types.data)
    guardrail = client.guardrails.create(
        name=f"{resource_prefix}-guardrail",
        description="created by Python SDK E2E",
        phases=["request"],
        scope="explicit",
        rule={"kind": "expression", "expression": "true", "on_false": "deny"},
        metadata={"suite": "orca-sdk-e2e"},
    )
    resources["guardrail"] = guardrail
    updated = client.guardrails.update(guardrail.id, description="updated by Python SDK E2E")
    assert updated.description == "updated by Python SDK E2E"
    assert client.guardrails.retrieve(guardrail.id).id == guardrail.id
    assert any(item.id == guardrail.id for item in client.guardrails.list(limit=100))

    prices = client.model_prices.list(limit=10)
    assert prices.data
    first = prices.data[0]
    retrieved = client.model_prices.retrieve(first.model_id, provider=first.provider)
    assert retrieved.to_dict() == first.to_dict()


def check_environment_and_agent() -> None:
    environment = client.environments.create(
        name=f"{resource_prefix}-environment",
        description="created by Python SDK E2E",
        config={"type": "cloud", "networking": {"type": "unrestricted"}},
    )
    resources["environment"] = environment
    updated_environment = client.environments.update(environment.id, description="updated by Python SDK E2E")
    assert updated_environment.description == "updated by Python SDK E2E"
    assert client.environments.retrieve(environment.id).id == environment.id
    assert any(item.id == environment.id for item in client.environments.list(limit=100))

    guardrail = resources.get("guardrail")
    if guardrail is None:
        agent = client.agents.create(
            name=f"{resource_prefix}-agent",
            model={"provider": PROVIDER, "id": MODEL_ID},
            system="Return concise answers.",
            metadata={"suite": "orca-sdk-e2e"},
        )
    else:
        agent = client.agents.create(
            name=f"{resource_prefix}-agent",
            model={"provider": PROVIDER, "id": MODEL_ID},
            system="Return concise answers.",
            metadata={"suite": "orca-sdk-e2e"},
            guardrail_ids=[guardrail.id],
            extra_headers=BETA_HEADERS,
        )
    resources["agent"] = agent
    updated = client.agents.update(agent.id, description="updated by Python SDK E2E", extra_headers=BETA_HEADERS)
    assert updated.description == "updated by Python SDK E2E"
    if guardrail is not None:
        assert updated.guardrail_ids == [guardrail.id]
        assert client.agents.retrieve(agent.id, extra_headers=BETA_HEADERS).guardrail_ids == [guardrail.id]
    assert any(item.id == agent.id for item in client.agents.list(limit=100, extra_headers=BETA_HEADERS))


def check_trigger() -> None:
    agent = resources["agent"]
    environment = resources["environment"]
    trigger = client.triggers.create(
        name=f"{resource_prefix}-trigger",
        agent={"type": "agent", "id": agent.id, "version": agent.version},
        session_mode="SESSION_PER_EVENT",
        source={
            "type": "cron",
            "schedule": "0 0 1 1 *",
            "timezone": "Etc/UTC",
            "payload": f"SDK trigger {run_suffix}",
        },
        session={
            "environment_id": environment.id,
            "title_template": "${trigger.name}",
            "metadata": {"suite": "orca-sdk-e2e"},
            "vault_ids": [],
        },
        replicas=1,
        paused=True,
    )
    resources["trigger"] = trigger
    assert trigger.status == "paused"
    assert client.triggers.retrieve(trigger.id).id == trigger.id
    updated = client.triggers.update(
        trigger.id,
        name=f"{resource_prefix}-trigger-updated",
        source={"type": "cron", "payload": f"Updated SDK trigger {run_suffix}"},
    )
    assert updated.name == f"{resource_prefix}-trigger-updated"
    assert updated.source.type == "cron"
    assert updated.source.payload == f"Updated SDK trigger {run_suffix}"
    assert any(item.id == trigger.id for item in client.triggers.list(agent_id=agent.id, limit=100))
    assert client.triggers.sessions.list(trigger.id, limit=10).data == []
    assert client.triggers.unpause(trigger.id).status == "active"
    paused = client.triggers.pause(trigger.id)
    assert paused.status == "paused"
    resources["trigger"] = paused


def check_file() -> None:
    content = f"orca-sdk e2e file {run_suffix}\n".encode()
    file = client.files.upload(file=(f"{resource_prefix}-upload.txt", content, "text/plain"))
    resources["file"] = file
    assert client.files.retrieve(file.id).id == file.id
    assert any(item.id == file.id for item in client.files.list(limit=100))
    try:
        client.files.download(file.id)
    except PermissionDeniedError:
        pass
    else:
        raise AssertionError("uploaded file unexpectedly allowed direct download")


def check_session() -> None:
    agent = resources["agent"]
    environment = resources["environment"]
    guardrail = resources.get("guardrail")
    agent_input: Any = agent.id
    if guardrail is not None:
        agent_input = {
            "type": "agent_with_overrides",
            "id": agent.id,
            "guardrail_ids": [guardrail.id],
        }
    session = client.sessions.create(
        agent=agent_input,
        environment_id=environment.id,
        title=f"{resource_prefix}-session",
        extra_headers=BETA_HEADERS if guardrail is not None else None,
    )
    resources["session"] = session
    assert client.sessions.retrieve(session.id).id == session.id
    assert any(item.id == session.id for item in client.sessions.list(agent_id=agent.id, limit=100))


def check_execution() -> None:
    session = resources["session"]
    marker = f"KIND_HELM_SDK_{run_suffix}"
    expected = f"MISSING_ECHO_TOOL {marker}"
    sent = client.sessions.events.send(
        session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": f"Return {marker}."}]}],
    )
    assert sent.data and len(sent.data) == 1
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        events = client.sessions.events.list(session.id, limit=1000, order="asc")
        if any(event.type == "agent.message" and expected in event.to_json() for event in events.data):
            break
        terminal = [
            event
            for event in events.data
            if event.type in {"session.error", "session.status_error", "session.setup_failed"}
        ]
        if terminal:
            raise RuntimeError(f"execution emitted terminal event: {terminal[0].to_json()}")
        time.sleep(1)
    else:
        raise TimeoutError(f"timed out waiting for deterministic reply: {expected}")

    with client.sessions.events.stream(session.id, from_cursor="0", timeout=10.0) as stream:
        if not any(expected in event.to_json() for event in stream):
            raise AssertionError("SSE replay did not include the deterministic reply")


def check_cloud() -> None:
    providers = client.cloud.agents.providers.list()
    assert any(provider.name == "orca-managed-agents" for provider in providers)
    provider = client.cloud.agents.providers.retrieve("orca-managed-agents")
    assert provider.api_key_configured is True
    assert isinstance(client.cloud.connections.list(), list)


try:
    run_scenario("extension discovery matches the topology", check_discovery)
    if not expect_cloud:
        run_scenario("policy and pricing extension APIs", check_policy_and_pricing)
    run_scenario("environment and agent lifecycle", check_environment_and_agent)
    run_scenario("trigger lifecycle and actions", check_trigger)
    run_scenario("file lifecycle and denied download", check_file)
    run_scenario("session creation and listing", check_session)
    if expect_execution:
        run_scenario("deterministic execution and SSE replay", check_execution)
    if expect_cloud:
        run_scenario("cloud provider and connection discovery", check_cloud)
    run_scenario("resource archival and deletion", lambda: cleanup_resources(True))
finally:
    cleanup_resources(False)
    client.close()

if failures:
    raise RuntimeError(f"{len(failures)} SDK E2E scenario(s) failed: {'; '.join(failures)}")
