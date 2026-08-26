"""Happy-path round trips against a live deployment.

These assert the shapes the SDK expects actually come back from a real server --
the thing hermetic tests cannot tell you, because they assert against fixtures we
wrote ourselves.
"""

from __future__ import annotations

from typing import Iterator

import pytest

from orca import Orca, ExtensionNotAvailableError
from orca.types import Agent

from .conftest import requires_credentials

pytestmark = requires_credentials


@pytest.fixture
def agent(client: Orca, run_prefix: str) -> Iterator[Agent]:
    created = client.agents.create(model="some-model", name=f"{run_prefix}-agent")
    try:
        yield created
    finally:
        # Archive rather than delete: agent deletion is not part of the portable surface.
        try:
            client.agents.archive(created.id)
        except Exception:  # noqa: BLE001 - cleanup must not mask a test failure
            pass


def test_discovery_lists_groups(client: Orca) -> None:
    groups = client.discovery.groups()
    # An empty list means "no extensions installed", which is a valid deployment.
    assert isinstance(groups.groups, list)


def test_agent_round_trip(client: Orca, agent: Agent) -> None:
    fetched = client.agents.retrieve(agent.id)
    assert fetched.id == agent.id
    assert fetched.type == "agent"
    assert fetched.version >= 1


def test_agent_update_is_version_checked(client: Orca, agent: Agent) -> None:
    updated = client.agents.update(agent.id, version=agent.version, description="updated")
    assert updated.version > agent.version


def test_agent_appears_in_list(client: Orca, agent: Agent) -> None:
    assert any(a.id == agent.id for a in client.agents.list())


def test_agent_versions_are_listed(client: Orca, agent: Agent) -> None:
    versions = list(client.agents.versions.list(agent.id))
    assert versions, "an agent always has at least its creation version"


def test_cloud_is_gated_consistently(client: Orca) -> None:
    """Cloud calls either work or raise the gate error -- never a raw 404."""
    groups = {g.name for g in client.discovery.groups().groups}
    if "cloud.sn.io" in groups:
        assert isinstance(client.cloud.agents.providers.list(), list)
    else:
        with pytest.raises(ExtensionNotAvailableError):
            client.cloud.agents.providers.list()
