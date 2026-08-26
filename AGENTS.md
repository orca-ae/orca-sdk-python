# orca-sdk-python — agent contributor guide

This guide is for any contributor (human or AI) adding code to `orca-sdk`. It captures the
conventions every contribution is expected to follow.

## 1. Source of truth

Two vendored OpenAPI specs plus the core deployment overlay define the portable SDK surface:

| Artifact | Base-path rule | Governs |
|---|---|---|
| `openapi/managed-agents.yaml` | No `servers` entry; paths carry `/v1`, `/api`, or `/apis` explicitly. | Core resources: `agents` (+`versions`), `sessions` (+`events`, `files`, `resources`, `threads(.events)`), `environments`, `files`, `skills` (+`versions`), `vaults` (+`credentials`), `memory_stores` (+`memories`, `memory_versions`), `triggers` (+`sessions`), `discovery`. |
| `openapi/managed-agents-deployment.overlay.yaml` | Applies to `managed-agents.yaml`. | Deployment deviations. Its removal actions define what is not portable across both supported backends. |
| `openapi/cloud-extensions.yaml` | `/apis/cloud.sn.io/v1` | The complete `cloud.*` namespace. |

These files are vendored byte-for-byte from the server that generates them. Never hand-edit
them; refresh them from the server instead.

Every public method maps 1:1 to an `operationId` in whichever spec governs it. We do not invent
operations, rename endpoints, or smuggle in extra fields. When a spec changes, the SDK changes —
not the other way around.

Applying the overlay's portability rules to core APIs:

- `remove: true` operations are not exposed.
- `remove_properties` fields are omitted from SDK request types.
- Removed query parameters are omitted from SDK parameter types.
- Operations whose responses are replaced with an unsupported response are not exposed.
- `x-deployment-query-parameter-extensions` are deployment-only; keep them out of common request
  types (this includes the top-level `provider` filters).
- `x-deployment-trigger-schema-extension` deliberately widens the core Trigger schemas. Preserve
  its sources, session modes, and replica range. The SDK does not preflight backend capabilities;
  a narrower backend returns its own API error.

## 2. Branding rule

This SDK does not reference any upstream vendor (company, product, codename, or third-party SDK)
anywhere in code, comments, docs, examples, tests, or commit messages. When you need to describe
lineage, say "this SDK" or point at a specific local file.

`./scripts/check-branding` enforces this over every tracked file and runs in CI. `openapi/` is
exempt because those are generated server artifacts, not our prose.

There is one in-source escape hatch, for **protocol constants only**: a value the server
defines and the SDK must send verbatim, such as an enum discriminator. Mark that single line
with `# wire-value` and the gate skips it. The rules:

- Per line, never per file.
- Only for values fixed by the contract. If we chose the string, it is not a wire value.
- Declare it once as a named alias and reference that everywhere else, so the literal appears
  in exactly one place (see `SkillSource` in `types/agent_shared.py`).
- Every active exemption is printed by the gate on each run, so they stay visible in CI
  rather than quietly accumulating.

## 3. Project layout

```
openapi/                 # vendored contracts (see §1)
src/orca/
  _client.py             # Orca / AsyncOrca — options, auth, resource mounts
  _base_client.py        # request pipeline, retries, pagination plumbing
  _models.py  _types.py  _exceptions.py  _constants.py  _compat.py
  _response.py  _streaming.py  _qs.py  _files.py  _resource.py  _utils/
  pagination.py
  resources/             # one module per flat resource, one package per resource with children
  types/                 # one file per request/response type
  lib/                   # higher-level conveniences built on resources
tests/                   # mirrors src/orca
scripts/                 # bootstrap / format / lint / test / check-branding
```

File naming is snake_case; resource classes are PascalCase (`MemoryStores` in
`memory_stores/memory_stores.py`).

## 4. Resource class pattern

Every resource ships four classes: `X(SyncAPIResource)`, `AsyncX(AsyncAPIResource)`,
`XWithRawResponse`, `XWithStreamingResponse` (plus the two async wrapper variants). Sub-resources
are `@cached_property` accessors constructed against `self._client`, never `self`.

Required pieces:

1. Methods call `self._get/._post/._put/._delete(...)` or `self._get_api_list(...)` for lists.
2. Paths with interpolation use `path_template("/v1/agents/{agent_id}", agent_id=agent_id)` —
   never f-strings or concatenation, so path segments are escaped.
3. Every path parameter is guarded:
   `if not agent_id: raise ValueError(f"Expected a non-empty value for \`agent_id\` but received {agent_id!r}")`
4. Every method ends with `extra_headers`, `extra_query`, `extra_body`, `timeout`.
5. Sync and async signatures must stay identical apart from `async`/`await`.

## 5. Path style

`base_url` is the **host root**. Every path literal carries its own full prefix.

- Core resources start with `/v1/...`.
- `cloud.*` resources start with `/apis/cloud.sn.io/v1/...`.
- Archive endpoints are `POST /.../{id}/archive` — never the colon form.
- Some cloud action endpoints do use a colon (`/foo:restart`). Mirror the spec literally.
- JSON fields stay snake_case; we mirror the wire shape.

## 6. HTTP-method mapping

Match the spec verb. Retrieve/list → `GET`; create and action endpoints → `POST`; full
replacement → `PUT`; partial update → `PATCH`; permanent delete → `DELETE`. If a verb looks
wrong, push back upstream rather than "correcting" it here.

## 7. Types

Responses are `BaseModel` subclasses; request params are `TypedDict, total=False` with `Required[]`
where the spec demands it.

**Aliasing a wire name uses a different mechanism on each, and getting it wrong fails silently:**

| Where | Mechanism |
|---|---|
| Request params (`TypedDict`) | `Annotated[T, PropertyInfo(alias="created_at[gt]")]` |
| Response models (`BaseModel`) | `pydantic.Field(default=None, alias="fieldName")` |

`PropertyInfo(alias=...)` on a response model does **not** raise — it silently yields `None`
for that field, forever. `tests/test_type_conventions.py` fails the build if one appears.

**Casing follows the wire, not a house style.** Core response attributes are snake_case because
the core wire format is; `cloud.*` response attributes are camelCase because *its* wire format
is. Both obey the same rule (§5, "we mirror the wire shape"), so the split between them is
intentional rather than drift. Method *arguments* are always snake_case — an argument is not a
wire field, and the wire key is applied at serialization. This is the same distinction the
TypeScript client draws when it writes `agentId` for an argument and `include_archived` for a
serialized field.

Naming: `Agent`, `AgentCreateParams`, `AgentUpdateParams`, `AgentListParams`, `DeletedAgent`.
Open shapes the server hasn't stabilised use `Dict[str, object]` with a one-line comment saying why.

Do **not** add a `beta_version` request-body field. No spec defines one, and sending it breaks
some backends. Beta opt-in is a header concern — every method already accepts
`extra_headers={"orca-beta": "..."}`.

## 8. Pagination

Two cursor shapes, both already implemented in `pagination.py`:

- Most lists send `page` and read `next_page` → `SyncPageCursor` / `AsyncPageCursor`.
- File lists send `after_id`/`before_id` and read `has_more`/`first_id`/`last_id` →
  `SyncPage` / `AsyncPage`.

Direction is preserved when auto-iterating: a `before_id` query follows `first_id`, otherwise it
follows `last_id`. Never mix the two directions in one request.

## 9. Streaming

SSE endpoints return `Stream[Event]` / `AsyncStream[Event]`. This API does **not** constrain event
names: every well-formed `data:` payload is yielded and callers discriminate on the payload's own
`type` field. `ping` is skipped, `error` raises, and a malformed frame is logged and skipped —
never raised.

## 10. Errors

- Raise `OrcaError` for client-side validation failures (missing config, malformed input).
- Server errors are produced by the request pipeline; subclasses are chosen by status code.
- `ExtensionNotAvailableError` is an `OrcaError`, **not** an `APIError` — no HTTP request is made
  for a gated call, so there is no response to attach.
- Never invent new error classes. The lineup is deliberately small and orthogonal.

## 11. Naming

- Clients: `Orca`, `AsyncOrca`.
- Environment variables: `ORCA_API_KEY`, `ORCA_BASE_URL`, `ORCA_LOG`. That is the whole list.
- Distribution `orca-sdk`; import `orca`.

## 12. Docstrings

Every public method gets a one-line summary and an `Args:` block. The last four entries are always
`extra_headers`, `extra_query`, `extra_body`, `timeout`, worded identically everywhere. Document
non-obvious *why* — optimistic concurrency, write-only fields, archive vs delete. Skip
"this creates an X" boilerplate.

## 13. Tests

- Unit tests live in `tests/api_resources/` mirroring `src/orca/resources/`, with `TestX` and
  `TestAsyncX` classes.
- HTTP is stubbed with `respx`. The suite is hermetic: no mock server, no network.
- Integration tests live in `tests/integration/` and are skipped unless `ORCA_TEST_API_KEY` and
  `ORCA_TEST_BASE_URL` are set.
- `tests/test_contract.py` diffs every `operationId` in the vendored specs against the SDK surface.
  Add new methods to its map or it fails.

## 14. Before opening a PR

```bash
./scripts/lint     # branding, ruff, pyright, mypy
./scripts/test     # pytest
```

Also confirm the surface doc and `CHANGELOG.md` reflect any new or changed methods.
