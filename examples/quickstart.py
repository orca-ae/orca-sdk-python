#!/usr/bin/env python
"""Create an environment and an agent, list agents, then archive.

Run with ORCA_BASE_URL and ORCA_API_KEY set.
"""

from __future__ import annotations

import sys

from orca import Orca, OrcaError


def main() -> None:
    client = Orca()

    environment = client.environments.create(name="quickstart-env")
    print(f"environment: {environment.id}")

    agent = client.agents.create(
        model="some-model",
        name="quickstart-agent",
        description="Created by examples/quickstart.py",
    )
    print(f"agent: {agent.id}")

    print("first few agents:")
    for index, existing in enumerate(client.agents.list()):
        print(f"  {existing.id}  {existing.name}")
        if index >= 4:
            break

    client.agents.archive(agent.id)
    print(f"archived {agent.id}")


if __name__ == "__main__":
    try:
        main()
    except OrcaError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(1) from err
