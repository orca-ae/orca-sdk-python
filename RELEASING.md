# Releasing

The SDK is published to [PyPI as `runorca`](https://pypi.org/project/runorca/), with
the same wheel and sdist attached to
[GitHub Releases](https://github.com/orca-ae/orca-sdk-python/releases). The Python
import remains `orca`.

**Release** (`.github/workflows/release.yml`) runs [release-please], which opens and
maintains a Release PR. Merging that PR creates the tag and GitHub Release, then
builds and publishes the distributions. The same workflow supports manual retries
for an existing release tag. It replaces `create-releases.yml` and
`publish-release.yml`; those old workflow names are no longer publishing entry points.

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

**A push of only hidden-type commits produces no release at all.** `test:` and `ci:` are
marked `hidden: true`, and release-please treats hidden types as non-user-facing: it skips
the release rather than cutting one with an empty changelog. The workflow still succeeds,
so a green run does not mean a release happened. If you expected one and got nothing, look
for this line in the **Release** workflow's **Prepare release** log:

```
✔ Considering: 1 commits
✔ No user facing commits found since <sha> - skipping
```

To ship a release whose commits are all hidden types, add a `Release-As: X.Y.Z` footer to
the final squash commit message. A footer present only in a branch commit or PR body
does not help if the squash merge discards it.

**The version lives in exactly one place: `[project].version` in `pyproject.toml`.**
`src/orca/_version.py` derives `__version__` from the installed distribution's metadata
via `importlib.metadata`, and `src/orca/__init__.py` re-exports it. Nothing is
hand-maintained, and the packaged version cannot drift from the version the client
reports. Do **not** add a version literal to `_version.py` — release-please has nothing to
rewrite there, and that is the point.

A git tag `v{version}` is created for every release. The publish step builds from that
exact tag.

## Typical flow

1. **Land work on `main`** by squash-merging a PR with a Conventional Commit title.
   The squash commit title is what release-please parses; a title such as
   `Merge pull request #123 ...` is not a Conventional Commit.
2. **release-please opens a Release PR** titled `release: X.Y.Z`, on every push to `main`
   and once a day at 05:00 UTC. It bumps `pyproject.toml`, regenerates `CHANGELOG.md`, and
   keeps updating the same PR as more commits land. A follow-up step pushes a
   `chore: sync uv.lock with the release version` commit to that branch.
3. **Review and merge the Release PR** when you want to ship. Merging it:
   - creates the tag `vX.Y.Z` and the GitHub Release,
   - builds and validates `runorca-X.Y.Z-py3-none-any.whl` and `runorca-X.Y.Z.tar.gz`,
   - publishes them to PyPI through Trusted Publishing, then attaches the same files
     to the GitHub Release.
4. **Repeat.** release-please starts a fresh Release PR as soon as the next commit lands.

Nothing else needs doing — there is no manual version bump and no hand-edited changelog.

### Bootstrapping the first public release

The initial import has version `0.2.1` in `.release-please-manifest.json` and
`pyproject.toml`, but that does not create a tag or GitHub Release. The first public
release uses the same Release PR flow as subsequent releases:

1. Squash-merge the bootstrap PR with its `feat:` title intact. With the `0.2.1`
   manifest baseline and the current versioning settings, this requests `0.3.0`.
2. **Release** opens the `release: 0.3.0` PR and refreshes `uv.lock` on its
   branch. Review its version, changelog, and CI results before merging.
3. Before merging, ensure the PyPI publishing changes are on `main` and the Release
   PR includes them: its distribution must be `runorca`, and the workflow must be
   `release.yml`. Merge that Release PR to create `v0.3.0`, the GitHub Release, and
   the PyPI release. Merging the bootstrap PR alone does not publish the package.

If **Prepare release** succeeds without opening a PR, inspect its log for
`commit could not be parsed` and `Considering: 0 commits`. A history containing only
an initial commit and a non-conventional merge commit can produce this result even
when the merged PR had a `feat:` title. Re-running the workflow without a new
parseable commit does not change the result.

Do not supply a manual `tag` for a version that has not been released: retries
require an existing tag and GitHub Release. Leave `tag` empty for the Release PR flow.

## Release workflow (`release.yml`)

**Triggers:**

| When | Trigger |
|------|---------|
| Every push to `main` | `push` |
| Daily 05:00 UTC | `schedule` cron |
| On demand | `workflow_dispatch` (optional `tag`) |

Preparation is guarded by repository `orca-ae/orca-sdk-python` and ref
`refs/heads/main`. Select **main** when manually running the workflow; other
branches and forks cannot drive publishing. Downstream jobs require preparation
to succeed and return a release tag.

**What it does:**

1. **Prepare release** runs `googleapis/release-please-action@v4` against
   `release-please-config.json` and `.release-please-manifest.json`. If it opens or
   updates a Release PR, it refreshes `uv.lock` on that branch. With a manual `tag`,
   it skips release-please and passes that tag directly to the build.
2. **Build and verify distributions** requires an existing GitHub Release and
   checks out `refs/tags/<tag>`, never a branch of the same name.
   `./scripts/build-release` builds with `uv build --no-sources`, checks both
   archives for the `runorca` name and matching tag version, verifies packaged
   licenses, and installs/imports the wheel in a fresh environment. This job has
   only `contents: read` and no OIDC permission.
3. **Publish runorca to PyPI** downloads those artifacts without checking out or
   executing repository code. Only this job has `id-token: write`. It runs
   `uv publish --trusted-publishing always --check-url https://pypi.org/simple`,
   requiring OIDC rather than falling back to a stored token.
4. **Attach the published distributions to GitHub** downloads the same artifacts
   and uploads them with `gh release upload --clobber`. It runs only after PyPI
   succeeds and has `contents: write`, but no OIDC permission.

This stays in a single workflow: tags created with `GITHUB_TOKEN` do not trigger
other workflows. Publishing does not depend on a tag-push or release event.

## Retrying a publication

| Input | Required | Purpose |
|-------|----------|---------|
| `tag` | no | Existing release tag to retry, e.g. `v0.3.0`; empty runs release-please |

Prefer **Re-run failed jobs** on the original run: it reuses the already-built
artifact. If a new run is needed, use **Release → Run workflow**, select `main`,
and supply the existing tag. The tag must contain the `runorca` packaging and
release scripts; historical tags for the old distribution cannot be published
as `runorca` without a new version.

uv skips files only when their bytes match the files already on PyPI. Different
contents under an existing filename fail rather than silently mixing artifacts.
If a rebuild differs after a partial upload, retry the original artifacts or cut
a new release; do not delete and attempt to reuse a PyPI filename. GitHub assets
are attached only after PyPI accepts or verifies the same files.

The build sets `SOURCE_DATE_EPOCH` from the tag commit to stabilize timestamps,
but dependencies or build-tool changes can still affect a later rebuild.

## Why the uv.lock step exists

`uv.lock` records the project's own version in its root package entry:

```toml
[[package]]
name = "runorca"
version = "0.1.0"
source = { editable = "." }
```

release-please bumps `pyproject.toml` but knows nothing about `uv.lock`, so the lock would
trail every release by one version. `./scripts/lint` runs `uv lock --check`, so a stale
lock fails CI on the Release PR — the refresh step keeps the PR self-consistent before
anyone reviews it.

`requirements-dev.lock` is unaffected: it pins `-e .` with no version and mentions
`runorca` only in `# via` comments.

## Consuming the package

Install from PyPI, or download the same wheel from the GitHub Release:

```sh
pip install runorca
python -c 'import orca; print(orca.__version__)'
```

Use `runorca==X.Y.Z` to pin a release. For unreleased changes, install
`"runorca @ git+https://github.com/orca-ae/orca-sdk-python@<commit>"`.
If this SDK was previously installed from Git as `orca-sdk`, uninstall that old
distribution first: installing both distributions creates overlapping `orca` files.

Do **not** run `pip install orca-sdk` — that name belongs to an unrelated package on
public PyPI.

## Required secrets / settings

GitHub release operations work with the default `secrets.GITHUB_TOKEN`. One optional
secret matters:

- **The release bot token (`SNBOT_GITHUB_TOKEN`)** — a PAT or GitHub App token with `contents: write` and
  `pull-requests: write`. GitHub does not run workflows for a PR opened by
  `GITHUB_TOKEN` (it suppresses them to prevent recursion), so **without this secret the
  Release PR gets no CI**. The workflow falls back to `GITHUB_TOKEN` via `||`, so it still
  functions — it just publishes something CI never checked.

If `main` is protected, the token also needs to be allowed to push the `uv.lock` commit to
the Release PR branch.

### PyPI Trusted Publisher

Configure these exact values in the PyPI account's **Publishing** page for the
pending project (or the project's **Publishing** settings after the first upload):

| Field | Value |
|-------|-------|
| PyPI project | `runorca` |
| GitHub repository owner | `orca-ae` |
| GitHub repository name | `orca-sdk-python` |
| Workflow filename | `release.yml` |
| Environment name | empty / Any |

No `PYPI_API_TOKEN` secret is needed. The workflow does not declare a GitHub
environment, matching the current publisher. Adding an environment with review
protection is a useful future hardening step, but must be coordinated with the
PyPI publisher settings.

A pending publisher does not reserve the name. The first successful publication
creates `runorca` and converts the publisher to a normal project publisher.

References: [PyPI pending publishers][pending-publishers],
[Trusted Publishing permissions][trusted-publishing], and
[uv publishing and hash-checked retries][uv-publishing]. uv does not generate
attestations itself; this workflow does not claim to produce signed attestations.

[pending-publishers]: https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/
[trusted-publishing]: https://docs.pypi.org/trusted-publishers/using-a-publisher/
[uv-publishing]: https://docs.astral.sh/uv/guides/package/#publishing-your-package

## Operational guidance

- **A release with no artifacts** can mean the build, PyPI upload, or GitHub upload
  failed after tagging. Check the failed job, fix the cause, and retry as above.
- **Re-publishing.** GitHub assets can be overwritten, but PyPI files are immutable.
  A code or artifact change requires a new version, not an in-place replacement.
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
