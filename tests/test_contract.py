"""Every operation in the vendored contract maps to a callable SDK method.

This is what catches a silently missed endpoint. It reads the spec rather than a
hand-written list, so an operation added upstream fails here until it is either
implemented or explicitly excluded with a reason.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from orca import Orca

SPEC = Path(__file__).parent.parent / "openapi" / "managed-agents.yaml"

# Operations the SDK deliberately does not expose. Each needs a reason, and each is
# also absent from the TypeScript client -- the two surfaces are kept in step.
NOT_EXPOSED = {
    # The deployment overlay replaces this response with an unsupported one.
    "agents.delete",
    # Removed outright by the deployment overlay.
    "gitCreds.resolveCreds",
    # Unauthenticated liveness probes, not part of the client surface.
    "health.healthz",
    "health.readyz",
    # `GET /api` reports core API versions; no client exposes it.
    "discovery.coreVersions",
    # No client exposes skill-version content download.
    "skills.getVersionContent",
    # No resource models outcomes yet.
    "outcomes.get",
}

# operationId -> dotted accessor on the client.
SDK_OPERATIONS: dict[str, str] = {
    "agents.archive": "agents.archive",
    "agents.create": "agents.create",
    "agents.get": "agents.retrieve",
    "agents.list": "agents.list",
    "agents.listVersions": "agents.versions.list",
    "agents.update": "agents.update",
    "discovery.groups": "discovery.groups",
    "environments.archive": "environments.archive",
    "environments.create": "environments.create",
    "environments.delete": "environments.delete",
    "environments.get": "environments.retrieve",
    "environments.list": "environments.list",
    "environments.update": "environments.update",
    "files.create": "files.upload",
    "files.delete": "files.delete",
    "files.get": "files.retrieve",
    "files.getContent": "files.download",
    "files.list": "files.list",
    "memoryStores.archive": "memory_stores.archive",
    "memoryStores.create": "memory_stores.create",
    "memoryStores.createMemory": "memory_stores.memories.create",
    "memoryStores.delete": "memory_stores.delete",
    "memoryStores.deleteMemory": "memory_stores.memories.delete",
    "memoryStores.get": "memory_stores.retrieve",
    "memoryStores.getMemory": "memory_stores.memories.retrieve",
    "memoryStores.getVersion": "memory_stores.memory_versions.retrieve",
    "memoryStores.list": "memory_stores.list",
    "memoryStores.listMemories": "memory_stores.memories.list",
    "memoryStores.listVersions": "memory_stores.memory_versions.list",
    "memoryStores.redactVersion": "memory_stores.memory_versions.redact",
    "memoryStores.update": "memory_stores.update",
    "memoryStores.updateMemory": "memory_stores.memories.update",
    "sessions.appendEvents": "sessions.events.send",
    "sessions.archive": "sessions.archive",
    "sessions.archiveThread": "sessions.threads.archive",
    "sessions.attachResource": "sessions.resources.add",
    "sessions.create": "sessions.create",
    "sessions.delete": "sessions.delete",
    "sessions.deleteFile": "sessions.files.delete",
    "sessions.detachResource": "sessions.resources.delete",
    "sessions.get": "sessions.retrieve",
    "sessions.getFile": "sessions.files.retrieve",
    "sessions.getFileContent": "sessions.files.download",
    "sessions.getResource": "sessions.resources.retrieve",
    "sessions.list": "sessions.list",
    "sessions.listEvents": "sessions.events.list",
    "sessions.listFiles": "sessions.files.list",
    "sessions.listResources": "sessions.resources.list",
    "sessions.listThreadEvents": "sessions.threads.events.list",
    "sessions.listThreads": "sessions.threads.list",
    "sessions.retrieveThread": "sessions.threads.retrieve",
    "sessions.streamEvents": "sessions.events.stream",
    "sessions.streamThread": "sessions.threads.events.stream",
    "sessions.update": "sessions.update",
    "sessions.updateResource": "sessions.resources.update",
    "skills.create": "skills.create",
    "skills.createVersion": "skills.versions.create",
    "skills.delete": "skills.delete",
    "skills.deleteVersion": "skills.versions.delete",
    "skills.get": "skills.retrieve",
    "skills.getVersion": "skills.versions.retrieve",
    "skills.list": "skills.list",
    "skills.listVersions": "skills.versions.list",
    "triggers.create": "triggers.create",
    "triggers.delete": "triggers.delete",
    "triggers.get": "triggers.retrieve",
    "triggers.list": "triggers.list",
    "triggers.pause": "triggers.pause",
    "triggers.sessions": "triggers.sessions.list",
    "triggers.unpause": "triggers.unpause",
    "triggers.update": "triggers.update",
    "vaults.archive": "vaults.archive",
    "vaults.archiveCredential": "vaults.credentials.archive",
    "vaults.create": "vaults.create",
    "vaults.createCredential": "vaults.credentials.create",
    "vaults.delete": "vaults.delete",
    "vaults.deleteCredential": "vaults.credentials.delete",
    "vaults.get": "vaults.retrieve",
    "vaults.getCredential": "vaults.credentials.retrieve",
    "vaults.list": "vaults.list",
    "vaults.listCredentials": "vaults.credentials.list",
    "vaults.mcpOauthValidateCredential": "vaults.credentials.validate",
    "vaults.update": "vaults.update",
    "vaults.updateCredential": "vaults.credentials.update",
}


def _spec_operation_ids() -> set[str]:
    return set(re.findall(r"^\s*operationId:\s*([\w.]+)\s*$", SPEC.read_text(), re.M))


def _resolve(client: Orca, dotted: str) -> object:
    target: object = client
    for part in dotted.split("."):
        target = getattr(target, part)
    return target


@pytest.fixture(scope="module")
def spec_ids() -> set[str]:
    return _spec_operation_ids()


def test_spec_is_vendored() -> None:
    assert SPEC.exists(), f"vendored contract missing at {SPEC}"


def test_every_operation_is_mapped_or_excluded(spec_ids: set[str]) -> None:
    unmapped = spec_ids - set(SDK_OPERATIONS) - NOT_EXPOSED
    assert not unmapped, (
        f"operations in the contract with no SDK method and no exclusion: {sorted(unmapped)}. "
        "Implement them, or add them to NOT_EXPOSED with a reason."
    )


def test_no_stale_mappings(spec_ids: set[str]) -> None:
    stale = set(SDK_OPERATIONS) - spec_ids
    assert not stale, f"mapped operations that no longer exist in the contract: {sorted(stale)}"


def test_no_stale_exclusions(spec_ids: set[str]) -> None:
    stale = NOT_EXPOSED - spec_ids
    assert not stale, f"excluded operations that no longer exist in the contract: {sorted(stale)}"


def test_every_mapping_is_callable() -> None:
    client = Orca(api_key="k", base_url="http://127.0.0.1:4010")
    for operation_id, dotted in sorted(SDK_OPERATIONS.items()):
        target = _resolve(client, dotted)
        assert callable(target), f"{operation_id} -> client.{dotted} is not callable"


def test_async_surface_matches_sync() -> None:
    """The two client trees must expose the same operations."""
    from orca import AsyncOrca

    client = AsyncOrca(api_key="k", base_url="http://127.0.0.1:4010")
    for operation_id, dotted in sorted(SDK_OPERATIONS.items()):
        target = _resolve(client, dotted)
        assert callable(target), f"{operation_id} -> async client.{dotted} is not callable"
