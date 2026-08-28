# Releasing

The SDK is distributed as wheel + sdist assets attached to
[GitHub Releases](https://github.com/orca-ae/orca-sdk-python/releases). Releases are
driven by two workflows in `.github/workflows/`:

- **`create-releases.yml`** — runs [release-please], which opens and maintains a Release
  PR; merging that PR tags the release and publishes the artifacts.
- **`publish-release.yml`** — manual re-run of just the build-and-attach step.

[release-please]: https://github.com/googleapis/release-please

## Versioning model

Versions are **derived from commit messages**, not chosen by hand. release-please reads
the [conventional commits] on `main` since the last release tag and computes the next
version:

| Commit prefix | Effect while at `0.x` |
|---------------|------------------------|
| `feat:` | minor bump (`0.1.0` → `0.2.0`) |
| `fix:`, `perf:`, `refactor:`, `revert:` | patch bump (`0.1.0` → `0.1.1`) |
| `docs:`, `chore:`, `style:`, `build:` | patch bump, listed in the changelog |
| `test:`, `ci:` | no release on their own; hidden from the changelog |
| `!` suffix or `BREAKING CHANGE:` footer | minor bump while `0.x`, major once `1.0.0` |

This is `bump-minor-pre-major: true` in `release-please-config.json` — correct for a
pre-1.0 SDK, where a breaking change should not burn the major version.

[conventional commits]: https://www.conventionalcommits.org/

**The version lives in exactly one place: `[project].version` in `pyproject.toml`.**
`src/orca/_version.py` derives `__version__` from the installed distribution's metadata
via `importlib.metadata`, and `src/orca/__init__.py` re-exports it. Nothing is
hand-maintained, and the packaged version cannot drift from the version the client
reports. Do **not** add a version literal to `_version.py` — release-please has nothing to
rewrite there, and that is the point.

A git tag `v{version}` is created for every release. The publish step builds from that
exact tag.

## Typical flow

1. **Land work on `main`** using conventional commit messages.
2. **release-please opens a Release PR** titled `release: X.Y.Z`, on every push to `main`
   and once a day at 05:00 UTC. It bumps `pyproject.toml`, regenerates `CHANGELOG.md`, and
   keeps updating the same PR as more commits land. A follow-up step pushes a
   `chore: sync uv.lock with the release version` commit to that branch.
3. **Review and merge the Release PR** when you want to ship. Merging it:
   - creates the tag `vX.Y.Z` and the GitHub Release,
   - triggers the build, which attaches `orca_sdk-X.Y.Z-py3-none-any.whl` and
     `orca_sdk-X.Y.Z.tar.gz` to that release.
4. **Repeat.** release-please starts a fresh Release PR as soon as the next commit lands.

Nothing else needs doing — there is no manual version bump and no hand-edited changelog.

## Create releases workflow (`create-releases.yml`)

**Triggers:**

| When | Trigger |
|------|---------|
| Every push to `main` | `push` |
| Daily 05:00 UTC | `schedule` cron |

Guarded by `if: github.repository == 'orca-ae/orca-sdk-python'` so a fork can never cut a
release.

**What it does:**

1. Runs `googleapis/release-please-action@v4` against `release-please-config.json` and
   `.release-please-manifest.json`.
2. If a Release PR was opened or updated — checks out that branch, runs `uv lock`, and
   pushes a commit if `uv.lock` changed. See "Why the uv.lock step exists" below.
3. If merging the Release PR created a release — checks out the new tag, runs
   `./scripts/publish-release` to build and attach the artifacts.

## Publish release workflow (`publish-release.yml`)

**Triggers:** `workflow_dispatch` only.

| Input | Required | Purpose |
|-------|----------|---------|
| `tag` | yes | Tag to build from and attach artifacts to, e.g. `v0.1.0` |

Use it when the release exists but has no artifacts — the publish step failed, or the tag
was created by hand. It checks out the given tag (never `main`) and runs the same
`./scripts/publish-release`. `gh release upload --clobber` makes a re-run idempotent, so
running it twice is safe.

## Why the uv.lock step exists

`uv.lock` records the project's own version in its root package entry:

```toml
[[package]]
name = "orca-sdk"
version = "0.1.0"
source = { editable = "." }
```

release-please bumps `pyproject.toml` but knows nothing about `uv.lock`, so the lock would
trail every release by one version. `./scripts/lint` runs `uv lock --check`, so a stale
lock fails CI on the Release PR — the refresh step keeps the PR self-consistent before
anyone reviews it.

`requirements-dev.lock` is unaffected: it pins `-e .` with no version and mentions
`orca-sdk` only in `# via` comments.

## Consuming the package

The repository is internal, so downloading a release asset needs a GitHub token with
`contents: read`. The `gh` CLI supplies one once you are logged in:

```sh
gh release download v0.1.0 --repo orca-ae/orca-sdk-python --pattern '*.whl'
uv pip install ./orca_sdk-0.1.0-py3-none-any.whl
```

To pin the SDK in a project, install from the tag instead:

```sh
uv pip install "orca-sdk @ git+ssh://git@github.com/orca-ae/orca-sdk-python@v0.1.0"
```

Do **not** run `pip install orca-sdk` — that name belongs to an unrelated package on
public PyPI.

## Required secrets / settings

Both workflows work with the default `secrets.GITHUB_TOKEN`. One optional secret matters:

- **`SNBOT_GITHUB_TOKEN`** — a PAT or GitHub App token with `contents: write` and
  `pull-requests: write`. GitHub does not run workflows for a PR opened by
  `GITHUB_TOKEN` (it suppresses them to prevent recursion), so **without this secret the
  Release PR gets no CI**. The workflow falls back to `GITHUB_TOKEN` via `||`, so it still
  functions — it just publishes something CI never checked.

If `main` is protected, the token also needs to be allowed to push the `uv.lock` commit to
the Release PR branch.

## Operational guidance

- **A release with no artifacts** means the publish step failed after the tag was created.
  Fix the cause, then run **Publish release** with that tag rather than re-cutting.
- **Re-publishing.** `gh release upload --clobber` overwrites assets in place, so a botched
  build can be replaced without a new version. Prefer a new patch release if the *code* was
  wrong, not just the upload.
- **Don't hand-edit `CHANGELOG.md` above the `## 0.1.0` entry.** release-please owns
  everything it generates and will rewrite it. The `## 0.1.0` prose block predates the
  automation and stays untouched.
- **Don't hand-edit the version in `pyproject.toml`.** release-please computes it from
  commits; editing it directly desynchronizes `.release-please-manifest.json`.
- **Manual local build.** To produce the artifacts without publishing:

  ```sh
  rm -rf dist
  uv build
  ```

  To verify one before shipping, install it into a scratch environment and import it:

  ```sh
  uv venv /tmp/verify
  VIRTUAL_ENV=/tmp/verify uv pip install dist/*.whl
  /tmp/verify/bin/python -c 'import orca; print(orca.__version__)'
  ```
