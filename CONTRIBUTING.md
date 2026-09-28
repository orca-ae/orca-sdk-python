# Contributing to the Orca Python SDK

Thanks for your interest in the Orca Python SDK. It is the Python client for the
[Orca Agent Engine](https://github.com/orca-ae/orca-agent-engine) API, imported as `orca`. Bug
reports, fixes, documentation, tests and feedback on the API are all welcome.

> **Using an AI assistant?** Read the [AI policy](AI_POLICY.md) first.
> **Are you a coding agent?** Start with [AGENTS.md](AGENTS.md).

## Ways to contribute

- **Report a bug or request a feature.** Open an
  [issue](https://github.com/orca-ae/orca-sdk-python/issues/new/choose).
- **Ask a question or share an idea.** Start a
  [discussion](https://github.com/orca-ae/orca-sdk-python/discussions).
- **Fix something.** Issues labeled
  [`good first issue`](https://github.com/orca-ae/orca-sdk-python/labels/good%20first%20issue) and
  [`help wanted`](https://github.com/orca-ae/orca-sdk-python/labels/help%20wanted) are good places to
  start. Comment on the issue to say you're working on it, so nobody duplicates your work.
- **Improve the docs.** If something confused you, it will confuse the next person too.
- **Report server behavior on the engine.** If a request misbehaves no matter which client sends it,
  the problem is in the server. Report it on the
  [engine repository](https://github.com/orca-ae/orca-agent-engine/issues).

## Where to talk

| For | Use |
|---|---|
| Bugs and concrete feature requests | [Issues](https://github.com/orca-ae/orca-sdk-python/issues) |
| Questions | [Discussions: Q&A](https://github.com/orca-ae/orca-sdk-python/discussions/categories/q-a) |
| Design ideas | [Discussions: Ideas](https://github.com/orca-ae/orca-sdk-python/discussions/categories/ideas) |
| Release news | [Discussions: Announcements](https://github.com/orca-ae/orca-sdk-python/discussions/categories/announcements) |
| Security vulnerabilities | Report privately, as described in the [security policy](https://github.com/orca-ae/.github/blob/main/SECURITY.md) |
| Conduct concerns | See the [code of conduct](https://github.com/orca-ae/.github/blob/main/CODE_OF_CONDUCT.md), or email conduct@runorca.ai |

The project doesn't run a Slack workspace or a mailing list, so decisions happen where everyone can
read them.

## Before you write code

- **Small, self-contained changes** can go straight to a pull request. Examples: a bug fix with a
  test, a documentation correction, a typo.
- **For anything larger**, open an issue or a discussion first. That includes a new helper, a
  refactor across modules, or a change in behavior. Agreeing on the approach first saves you from
  writing code that has to be redone.
- **API changes start in the engine.** This SDK follows the engine's API contract. Every public
  method maps one to one to an `operationId` in the OpenAPI specs vendored under
  [`openapi/`](openapi/). We don't invent operations, rename endpoints, or send fields the spec
  doesn't define. A new endpoint, field or server behavior is proposed on the
  [engine repository](https://github.com/orca-ae/orca-agent-engine), and lands here once the spec
  ships.

## Build and test

You need Python 3.10 or later and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/orca-ae/orca-sdk-python.git
cd orca-sdk-python
./scripts/bootstrap    # install Python with uv and sync the dev dependencies
./scripts/test         # pytest
```

The test suite is hermetic. Every HTTP interaction is stubbed with
[respx](https://lundberg.github.io/respx/), so it needs no server, no credentials and no network.
`./scripts/test` passes its arguments through to pytest, so `./scripts/test tests/test_client.py -k
retry` runs a subset.

Integration tests in `tests/integration` call a live engine. They are skipped unless both variables
are set:

```bash
ORCA_TEST_API_KEY=... ORCA_TEST_BASE_URL=... ./scripts/test tests/integration
```

Before you open a pull request, run the same checks CI runs:

```bash
./scripts/format   # ruff format, then ruff check --fix
./scripts/lint     # branding and license-header checks, uv.lock check, ruff, pyright, mypy
./scripts/test
```

## How the code is organized

```text
orca-sdk-python/
├── openapi/              # Vendored API contracts: the source of truth for the public surface
├── src/orca/
│   ├── _client.py        # Orca and AsyncOrca: options, auth, resource mounts
│   ├── _base_client.py   # Request pipeline, retries, pagination plumbing
│   ├── resources/        # One module per resource, one package per resource with children
│   ├── types/            # One file per request or response type
│   └── lib/              # Higher-level helpers built on the resources
├── tests/                # Mirrors src/orca; tests/api_resources/ mirrors src/orca/resources/
├── examples/             # Runnable examples
└── scripts/              # bootstrap, format, lint, test, and the repository checks
```

[AGENTS.md](AGENTS.md) is the full guide to the conventions: where the specs come from, the resource
class pattern, path style, types, pagination, streaming and errors. Read §1 and §4 before you add a
resource. That's where mistakes are most expensive.

## Code style

Ruff formats and lints the code, and pyright and mypy type-check it. The rest comes up in review.

- Every source file starts with the repository license header, after any shebang line:

  ```python
  # Copyright The Orca Authors
  # SPDX-License-Identifier: Apache-2.0
  ```

  `./scripts/check-license-headers --fix` adds it. The file
  `src/orca/_utils/_utils.py` contains MPL code and instead carries
  `Apache-2.0 AND MIT AND MPL-2.0`; preserve that expression and its MPL notice.
  The header check enforces this exception.
- Sync and async methods keep identical signatures, apart from `async` and `await`.
- Build request paths with `path_template(...)`, never with f-strings or concatenation.
- Mirror the wire shape. JSON fields keep the names the spec gives them.
- `./scripts/check-branding` runs as part of lint. [AGENTS.md](AGENTS.md) §2 explains what it
  checks and how to handle a protocol constant.

## Tests

- Add a test for the behavior you change.
- Unit tests for a resource live in `tests/api_resources/`, mirroring `src/orca/resources/`, with a
  sync and an async test class. Stub HTTP with respx; tests never reach the network.
- `tests/test_contract.py` compares the SDK surface with every `operationId` in the vendored specs.
  When you add a method, add it to the test's map, or the test fails.

## Commits

### Sign your commits (DCO)

Every commit needs a Developer Certificate of Origin sign-off:

```bash
git commit -s -m "fix: keep the query string when following next_page"
```

The `-s` flag adds a line such as `Signed-off-by: Your Name <you@example.com>`. The line certifies
that you wrote the change, or otherwise have the right to submit it under the project's license. The
full text is at [developercertificate.org](https://developercertificate.org/).

A DCO check runs on every pull request. If you forgot to sign off, fix the last commit with
`git commit --amend -s --no-edit`, or a series with `git rebase --signoff origin/main`, and then
force-push your branch.

We don't use a CLA. The DCO sign-off is all we ask.

### Write Conventional Commit messages

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`,
`fix:`, `docs:`, `refactor:`, `test:`, `ci:` or `chore:`, then a short summary in the imperative
mood. Mark an incompatible change with `!` after the type (`feat!: ...`) and a `BREAKING CHANGE:`
footer that says what users must change. Then explain why the change is needed, if that isn't
obvious.

This matters more than usual here. Release automation reads the messages on `main` to choose the
next version and write the changelog. Pull requests are squash-merged, so the pull request title
becomes the commit subject on `main`: write the title as a Conventional Commit too. Don't edit
`CHANGELOG.md` or the version by hand; the release pull request does both.

### Say when AI helped

If an AI tool helped meaningfully, add an `Assisted-by:` trailer that names the tool. The
[AI policy](AI_POLICY.md) explains what counts.

## Pull requests

1. Fork the repository on GitHub, and add your fork as a remote:
   `git remote add fork https://github.com/<your-username>/orca-sdk-python.git`. Create a branch for
   your change, and push it to `fork`.
2. Keep each pull request to one logical change. Smaller pull requests get reviewed sooner.
3. Fill in the pull request template: what changed and why, compatibility, how you tested it, and AI
   assistance.
4. Update `README.md`, `api.md` and the docstrings in the same pull request when you change the
   public surface.
5. Make sure CI passes.
6. A code owner for the files you touched reviews and approves the change. Code owners are listed in
   [CODEOWNERS](.github/CODEOWNERS). These docs call them maintainers.

We aim to respond promptly. If your pull request has been quiet for a while, @-mention one of the
code owners for the files you changed.

Maintainers cut releases from `main`. [RELEASING.md](RELEASING.md) describes the process.

## License

The Orca Python SDK is licensed under the [Apache License 2.0](LICENSE), and so is your
contribution. Parts of the SDK are derived from other open source projects. [NOTICE](NOTICE) and
[THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) list them, with their licenses.
