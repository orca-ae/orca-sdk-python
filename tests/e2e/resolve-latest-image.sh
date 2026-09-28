#!/usr/bin/env bash
# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "${SCRIPT_DIR}/lib.sh"

e2e::require_env SOURCE_IMAGE
e2e::require_command docker
e2e::require_command jq

source_tag=${SOURCE_TAG:-latest}
requested_image="${SOURCE_IMAGE}:${source_tag}"
image_platform=${IMAGE_PLATFORM:-linux/amd64}
image_component=${IMAGE_COMPONENT:-Managed Agents}
IFS=/ read -r platform_os platform_arch platform_variant extra <<<"${image_platform}"
if [[ -z "${platform_os}" || -z "${platform_arch}" || -n "${extra:-}" ]]; then
  echo "invalid image platform: ${image_platform}" >&2
  exit 1
fi

manifest=$(docker buildx imagetools inspect "${requested_image}" --format '{{json .Manifest}}')
digest=$(jq -r \
  --arg os "${platform_os}" \
  --arg arch "${platform_arch}" \
  --arg variant "${platform_variant:-}" \
  '.manifests[]
    | select(.platform.os == $os and .platform.architecture == $arch)
    | select($variant == "" or .platform.variant == $variant)
    | .digest' <<<"${manifest}" | head -n 1)
if [[ ! "${digest}" =~ ^sha256:[0-9a-f]{64}$ ]]; then
  echo "failed to resolve ${requested_image} for ${image_platform} to an immutable digest" >&2
  exit 1
fi

resolved_image="${SOURCE_IMAGE}@${digest}"
image_config=$(docker buildx imagetools inspect \
  "${resolved_image}" --format '{{json .Image}}')
revision=$(jq -r \
  '.config.Labels["org.opencontainers.image.revision"] // "unknown"' \
  <<<"${image_config}")
created=$(jq -r '.created' <<<"${image_config}")
if [[ -z "${revision}" || "${revision}" == "<no value>" ]]; then
  revision=unknown
fi

# The revision names a commit in a private repository. Mask it before anything can print it:
# workflow logs in this repository are public.
if [[ "${GITHUB_ACTIONS:-}" == "true" && "${revision}" != "unknown" ]]; then
  echo "::add-mask::${revision}"
fi

if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  {
    echo "source_image=${requested_image}"
    echo "resolved_image=${resolved_image}"
    echo "digest=${digest}"
    echo "revision=${revision}"
    echo "platform=${image_platform}"
  } >>"${GITHUB_OUTPUT}"
fi

printf 'resolved the %s image (created %s) to an immutable digest\n' "${image_component}" "${created}"
