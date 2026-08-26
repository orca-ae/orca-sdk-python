#!/usr/bin/env python
"""Send a message to a session and stream its events until the session goes idle.

Run with ORCA_BASE_URL and ORCA_API_KEY set.
"""

from __future__ import annotations

import sys
import time

from orca import Orca, OrcaError

DEADLINE_SECONDS = 30


def main() -> None:
    client = Orca()

    environment = client.environments.create(name="streaming-env")
    agent = client.agents.create(model="some-model", name="streaming-agent")
    session = client.sessions.create(agent=agent.id, environment_id=environment.id)
    print(f"session: {session.id}")

    client.sessions.events.send(
        session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": "Hello"}]}],
    )

    deadline = time.monotonic() + DEADLINE_SECONDS
    for event in client.sessions.events.stream(session.id):
        print(f"  {event.type}")
        if event.type == "session.status_idle":
            break
        if time.monotonic() > deadline:
            print(f"  (stopping after {DEADLINE_SECONDS}s)")
            break

    client.sessions.archive(session.id)
    client.agents.archive(agent.id)


if __name__ == "__main__":
    try:
        main()
    except OrcaError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(1) from err
