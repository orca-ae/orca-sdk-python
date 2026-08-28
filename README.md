# Orca Python SDK

Python client for the [Orca Agent Engine](https://github.com/orca-ae/orca-managed-agents) API.

## Installation

Releases are published as assets on this repository's [GitHub
Releases](https://github.com/orca-ae/orca-sdk-python/releases). The repository is
internal, so installing needs a GitHub token with `contents: read` — the `gh` CLI
supplies one once you are logged in:

```sh
gh release download v0.1.0 --repo orca-ae/orca-sdk-python --pattern '*.whl'
uv pip install ./orca_sdk-0.1.0-py3-none-any.whl
```

To pin the SDK in a project, install straight from the tag instead:

```sh
uv pip install "orca-sdk @ git+ssh://git@github.com/orca-ae/orca-sdk-python@v0.1.0"
```

> **Note:** do not run `pip install orca-sdk` — that name belongs to an unrelated
> package on public PyPI.

## Usage

```python
import os
from orca import Orca

client = Orca(
    api_key=os.environ.get("ORCA_API_KEY"),
    base_url=os.environ.get("ORCA_BASE_URL"),
)

agent = client.agents.create(model="some-model", name="My First Agent")
print(agent.id)
```

Every method is available on an async client with the same signature:

```python
import asyncio
from orca import AsyncOrca

client = AsyncOrca()


async def main() -> None:
    agent = await client.agents.create(model="some-model", name="My First Agent")
    print(agent.id)


asyncio.run(main())
```

## Configuration

| Option | Environment variable | Default |
|---|---|---|
| `api_key` | `ORCA_API_KEY` | — |
| `base_url` | `ORCA_BASE_URL` | required |
| `timeout` | — | 600 seconds |
| `max_retries` | — | 2 |

`base_url` is the **host root**. The SDK writes the `/v1/...` and `/apis/...` prefixes
itself, so pass `https://orca.example`, not `https://orca.example/v1`. A trailing `/v1`,
`/v1/registry`, or `/api/v1` is stripped with a deprecation warning.

There is no default host: this API is self-hosted, so a missing base URL raises rather
than silently pointing somewhere unexpected.

### Credentials

```python
# A literal token
client = Orca(api_key="sk-...")

# Resolved per request -- the hook for short-lived or rotating tokens
client = Orca(api_key=lambda: read_current_token())

# No Authorization header, for a deployment behind an authenticating proxy
client = Orca(api_key=None)
```

The async client also accepts a coroutine function.

## Pagination

List methods return a page that iterates across page boundaries automatically:

```python
for agent in client.agents.list():
    print(agent.id)
```

```python
async for agent in client.agents.list():
    print(agent.id)
```

To handle pages yourself:

```python
page = client.agents.list(limit=20)
print(page.data, page.next_page)
```

## Streaming

Session events arrive as server-sent events:

```python
session = client.sessions.create(agent="agent_id", environment_id="env_id")

client.sessions.events.send(
    session.id,
    events=[{"type": "user.message", "content": [{"type": "text", "text": "Hello"}]}],
)

for event in client.sessions.events.stream(session.id):
    if event.type == "session.status_idle":
        break
```

Event names are not constrained by the SDK: every well-formed frame is yielded and you
discriminate on the payload's own `type`.

## Working with one session

`client.session(id)` returns a handle that carries the session id for you:

```python
handle = client.session("session_123")

handle.events.send(events=[{"type": "user.message", "content": [...]}])

for thread in handle.threads.list():
    print(thread.id)

response = handle.files.download("file_123")
```

## File uploads

```python
metadata = client.files.upload(file=("hello.txt", b"hello\n", "text/plain"))
```

Anything accepted by `FileTypes` works: bytes, a file object, a path, or a
`(filename, content, content_type)` tuple.

## Errors

```python
from orca import Orca, OrcaError, APIError, NotFoundError, RateLimitError

try:
    client.agents.retrieve("missing_id")
except NotFoundError as err:
    print("not found:", err.status_code)
except RateLimitError as err:
    print("rate limited; retry-after:", err.headers.get("retry-after"))
except APIError as err:
    print(err.status_code, err.message)
except OrcaError as err:
    print("client-side error:", err)
```

| Class | Status |
|---|---|
| `BadRequestError` | 400 |
| `AuthenticationError` | 401 |
| `PermissionDeniedError` | 403 |
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `UnprocessableEntityError` | 422 |
| `RateLimitError` | 429 |
| `InternalServerError` | 5xx |
| `APIConnectionError` | network |
| `APIConnectionTimeoutError` | timeout |
| `ExtensionNotAvailableError` | client-side gate |

## Cloud extensions

Methods under `client.cloud.*` are served by a deployment-specific extension group. On a
deployment that does not serve it, they raise before making any request:

```python
from orca import ExtensionNotAvailableError

try:
    providers = client.cloud.agents.providers.list()
except ExtensionNotAvailableError as err:
    print(f"this deployment has no {err.group!r} extension installed")
```

To check first:

```python
groups = client.discovery.groups()
if any(g.name == "cloud.sn.io" for g in groups.groups):
    ...
```

## Retries and timeouts

Failed requests are retried twice by default, with exponential backoff honouring
`retry-after`. Connection errors, timeouts, 408, 409, 429, and 5xx are retried.

```python
client = Orca(max_retries=3, timeout=30.0)

client.agents.list(timeout=5.0)  # per request
```

## Accessing the raw response

```python
response = client.agents.with_raw_response.list()
print(response.headers.get("request-id"))
agents = response.parse()
```

`with_streaming_response` defers reading the body:

```python
with client.agents.with_streaming_response.list() as response:
    print(response.headers)
    agents = response.parse()
```

## Versioning

This package follows semantic versioning. Internal names prefixed with an underscore are
not part of the public surface.

## Contributing

See [`AGENTS.md`](AGENTS.md) for the conventions every contribution follows.

```sh
./scripts/bootstrap
./scripts/test
./scripts/lint
```

## License

Apache-2.0
