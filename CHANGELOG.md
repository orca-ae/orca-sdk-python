# Changelog

## 0.1.0

First release. Python client for the Orca Agent Engine API, at parity with the
TypeScript client: **179 public methods** across the core API and the cloud
extension group, on both a synchronous and an asynchronous client.

### Core API — 84 methods

`agents` (+`versions`), `sessions` (+`events`, `files`, `resources`,
`threads`(+`events`)), `environments`, `files`, `skills` (+`versions`),
`vaults` (+`credentials`), `memory_stores` (+`memories`, `memory_versions`),
`triggers` (+`sessions`), `discovery`.

### Cloud extensions — 95 methods

`cloud.connectors` (`sinks`, `sources`, `kafka`(+`plugins`, `connectors`)),
`cloud.functions`, `cloud.connections`, `cloud.packages`, `cloud.catalog`,
`cloud.agents.providers`, `cloud.health`, `cloud.api_resources`.

Every method under `cloud.*` resolves the deployment's extension groups first and
raises `ExtensionNotAvailableError` -- without issuing a request -- when the group
is not served.

### Client

- `base_url` is the host root and is required; a legacy `/v1`, `/v1/registry`, or
  `/api/v1` suffix is stripped with a warning.
- `api_key` accepts a literal, or a callable resolved per request for short-lived
  and rotating credentials. The async client also accepts a coroutine.
- `client.session(id)` returns a handle whose sub-resources carry the session id.
- Sync and async clients, each with `.with_raw_response` and
  `.with_streaming_response`.
- Automatic cursor pagination over both cursor styles the API uses.
- Server-sent events with no event-name allowlist: every well-formed frame is
  yielded and callers discriminate on the payload's own `type`.

### Verification

`tests/test_contract.py` and `tests/test_cloud_contract.py` check the surface
against the vendored contracts, so a missed or drifted endpoint fails the build
rather than shipping. `tests/integration/` runs against a live deployment when
`ORCA_TEST_API_KEY` and `ORCA_TEST_BASE_URL` are set, and is skipped otherwise.
