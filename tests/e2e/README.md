# End-to-end tests

The two workflows exercise the Python SDK against the same deployment topologies
as the TypeScript SDK:

- `e2e-managed-agents.yml` installs Managed Agents with Helm and connects directly
  with a workspace API key.
- `e2e-registry-provider.yml` deploys the Registry provider topology and connects
  through its OAuth-protected endpoint using `streamnative/registry-service:v1.0.2`.

Both workflows pin the paired Registry and Harness images in `dependencies.env`,
resolve their immutable digests, and check out the matching Helm chart revision.
They build and install the current SDK wheel before running the shared Python
scenario, which covers extension discovery, Guardrail lifecycle,
Agent and Session guardrail attachment, Model Price reads, Environment, Trigger,
File, and Session lifecycle calls, deterministic execution with SSE replay, and
cloud discovery where available.

Both topologies clean up Sessions with `POST /v1/sessions/{id}/archive` and
verify the returned Session ID and `archived_at`. Session cleanup does not call
DELETE, which the Registry's Orca provider disables.

Both topologies pull their pinned MinIO server and client releases from
`quay.io/minio` because anonymous Docker Hub pulls fail for these images. The
Registry/provider workflow rewrites the image repository in its pinned Registry
fixture before applying it, preserving the fixture's release tags.

The direct workflow requires `SNBOT_GITHUB_TOKEN`. The Registry/provider workflow
also requires `LICENSE`, `OAUTH_CLIENT_ID`, and `OAUTH_CLIENT_SECRET`. Secret-backed
jobs skip fork pull requests.
