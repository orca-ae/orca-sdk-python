# Contract provenance

`managed-agents.yaml` was refreshed on 2026-09-09 from the published SDK core
artifact, without editing or reserializing its bytes:

- TypeScript: `orca-ae/orca-sdk-typescript` revision
  `02d7e2d832ad667a7b5af20493677b2d615c1f8a`, `openapi/managed-agents.yaml`.
- Identical Go artifact: `orca-ae/orca-sdk-go` revision
  `c279d4b755650c10a2f158bfc170df73a6772340`, same path.
- SHA-256: `5320b32f415cb7e73383323dcdcdc3a5d36c418dfc73cca590a5e520ab3ce984`.

Server verification used `orca-ae/orca-managed-agents` revision
`9d8df4b18bdc3a32bbe903a69cd9c9a846083283`,
`services/registry-service-ts/openapi/managed-agents.yaml`. All nine
`guardrail_ids` property definitions agree with that server contract.

The published SDK core artifact is **not** a byte-for-byte copy of the current
combined server artifact (SHA-256
`d4e2234ffef123a49765acd7661c65b59a430ec60e30d0b2c508b635d751ec2f`).
The server includes policy/pricing operations split into a separate SDK spec,
additional environment/session operations, and other shared-path differences.
This refresh preserves the existing published SDK contract boundary rather than
silently importing those unrelated changes. A fully server-identical refresh
requires coordinated contract publishing across SDKs; this file records the
current exception to the contributor guide's byte-for-byte server provenance rule.
