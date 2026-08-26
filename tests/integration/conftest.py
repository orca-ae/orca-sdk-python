"""Live-API integration tests.

Skipped entirely unless `ORCA_TEST_API_KEY` and `ORCA_TEST_BASE_URL` are set, so a
normal `./scripts/test` run stays hermetic and needs no credentials.

Everything these tests create is named with a per-run prefix and archived or deleted
afterwards, so a crashed run leaves identifiable debris rather than anonymous junk.
"""

from __future__ import annotations

import os
import uuid
from typing import Iterator

import pytest

from orca import Orca

API_KEY = os.environ.get("ORCA_TEST_API_KEY")
BASE_URL = os.environ.get("ORCA_TEST_BASE_URL")

requires_credentials = pytest.mark.skipif(
    not (API_KEY and BASE_URL),
    reason="set ORCA_TEST_API_KEY and ORCA_TEST_BASE_URL to run integration tests",
)


@pytest.fixture(scope="session")
def run_prefix() -> str:
    """A per-run marker so resources this suite creates are identifiable."""
    return f"it-{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def client() -> Iterator[Orca]:
    if not (API_KEY and BASE_URL):
        pytest.skip("integration credentials not configured")
    with Orca(api_key=API_KEY, base_url=BASE_URL) as client:
        yield client
