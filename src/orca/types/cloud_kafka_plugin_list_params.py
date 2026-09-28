# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CloudKafkaPluginListParams"]


class CloudKafkaPluginListParams(TypedDict, total=False):
    connectorsOnly: bool
    """List only connector plugins instead of every plugin the worker has loaded."""
