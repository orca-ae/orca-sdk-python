"""Ergonomic handle for working with a single session.

`client.session(session_id)` returns a handle whose sub-resources already carry the
session id, so it does not have to be repeated on every call:

```python
handle = client.session("session_123")
handle.events.send(events=[...])
for event in handle.events.stream():
    ...
```

The handle holds no state beyond the id and performs no I/O when constructed -- it is
pure argument currying over the same resources reachable at `client.sessions.*`, so
building one per call site is as cheap as reusing one.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from functools import partial

from .._compat import cached_property

if TYPE_CHECKING:
    from .._client import Orca, AsyncOrca

__all__ = ["SessionHandle", "AsyncSessionHandle"]


class _EventsHandle:
    def __init__(self, client: Orca, session_id: str) -> None:
        events = client.sessions.events
        self.list = partial(events.list, session_id)
        self.send = partial(events.send, session_id)
        self.stream = partial(events.stream, session_id)


class _FilesHandle:
    def __init__(self, client: Orca, session_id: str) -> None:
        files = client.sessions.files
        self.list = partial(files.list, session_id)
        self.retrieve = partial(files.retrieve, session_id)
        self.download = partial(files.download, session_id)
        self.delete = partial(files.delete, session_id)


class _ResourcesHandle:
    def __init__(self, client: Orca, session_id: str) -> None:
        resources = client.sessions.resources
        self.list = partial(resources.list, session_id)
        self.add = partial(resources.add, session_id)
        self.retrieve = partial(resources.retrieve, session_id)
        self.update = partial(resources.update, session_id)
        self.delete = partial(resources.delete, session_id)


class _ThreadEventsHandle:
    def __init__(self, client: Orca, session_id: str) -> None:
        events = client.sessions.threads.events
        self.list = partial(events.list, session_id)
        self.stream = partial(events.stream, session_id)


class _ThreadsHandle:
    def __init__(self, client: Orca, session_id: str) -> None:
        threads = client.sessions.threads
        self.list = partial(threads.list, session_id)
        self.retrieve = partial(threads.retrieve, session_id)
        self.archive = partial(threads.archive, session_id)
        self.events = _ThreadEventsHandle(client, session_id)


class SessionHandle:
    """A session's sub-resources with the session id already applied."""

    session_id: str

    def __init__(self, client: Orca, session_id: str) -> None:
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        self._client = client
        self.session_id = session_id

    @cached_property
    def events(self) -> _EventsHandle:
        return _EventsHandle(self._client, self.session_id)

    @cached_property
    def files(self) -> _FilesHandle:
        return _FilesHandle(self._client, self.session_id)

    @cached_property
    def resources(self) -> _ResourcesHandle:
        return _ResourcesHandle(self._client, self.session_id)

    @cached_property
    def threads(self) -> _ThreadsHandle:
        return _ThreadsHandle(self._client, self.session_id)


class _AsyncEventsHandle:
    def __init__(self, client: AsyncOrca, session_id: str) -> None:
        events = client.sessions.events
        self.list = partial(events.list, session_id)
        self.send = partial(events.send, session_id)
        self.stream = partial(events.stream, session_id)


class _AsyncFilesHandle:
    def __init__(self, client: AsyncOrca, session_id: str) -> None:
        files = client.sessions.files
        self.list = partial(files.list, session_id)
        self.retrieve = partial(files.retrieve, session_id)
        self.download = partial(files.download, session_id)
        self.delete = partial(files.delete, session_id)


class _AsyncResourcesHandle:
    def __init__(self, client: AsyncOrca, session_id: str) -> None:
        resources = client.sessions.resources
        self.list = partial(resources.list, session_id)
        self.add = partial(resources.add, session_id)
        self.retrieve = partial(resources.retrieve, session_id)
        self.update = partial(resources.update, session_id)
        self.delete = partial(resources.delete, session_id)


class _AsyncThreadEventsHandle:
    def __init__(self, client: AsyncOrca, session_id: str) -> None:
        events = client.sessions.threads.events
        self.list = partial(events.list, session_id)
        self.stream = partial(events.stream, session_id)


class _AsyncThreadsHandle:
    def __init__(self, client: AsyncOrca, session_id: str) -> None:
        threads = client.sessions.threads
        self.list = partial(threads.list, session_id)
        self.retrieve = partial(threads.retrieve, session_id)
        self.archive = partial(threads.archive, session_id)
        self.events = _AsyncThreadEventsHandle(client, session_id)


class AsyncSessionHandle:
    """A session's sub-resources with the session id already applied."""

    session_id: str

    def __init__(self, client: AsyncOrca, session_id: str) -> None:
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        self._client = client
        self.session_id = session_id

    @cached_property
    def events(self) -> _AsyncEventsHandle:
        return _AsyncEventsHandle(self._client, self.session_id)

    @cached_property
    def files(self) -> _AsyncFilesHandle:
        return _AsyncFilesHandle(self._client, self.session_id)

    @cached_property
    def resources(self) -> _AsyncResourcesHandle:
        return _AsyncResourcesHandle(self._client, self.session_id)

    @cached_property
    def threads(self) -> _AsyncThreadsHandle:
        return _AsyncThreadsHandle(self._client, self.session_id)
