# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import runpy
from pathlib import Path

CHECKER = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/check-license-headers"))
MIXED_FILE = "src/orca/_utils/_utils.py"


def test_mixed_license_file_rejects_apache_only_header() -> None:
    data = CHECKER["HEADER"] + b"\n# Existing third-party notice\nvalue = 'kept'\r\n"
    assert not CHECKER["has_header"](data, MIXED_FILE)
    fixed = CHECKER["with_header"](data, MIXED_FILE)
    assert CHECKER["has_header"](fixed, MIXED_FILE)
    assert fixed.count(b"SPDX-License-Identifier:") == 1
    assert fixed.endswith(b"\n# Existing third-party notice\nvalue = 'kept'\r\n")
    assert CHECKER["with_header"](fixed, MIXED_FILE) == fixed


def test_license_override_does_not_apply_to_other_files() -> None:
    data = CHECKER["expected_header"](MIXED_FILE)
    assert not CHECKER["has_header"](data, "src/orca/_client.py")
    assert CHECKER["has_header"](CHECKER["HEADER"], "src/orca/_client.py")


def test_fix_preserves_shebang_and_existing_notices() -> None:
    data = b"#!/usr/bin/env python3\n# Existing attribution\nprint('example')\r\n"
    fixed = CHECKER["with_header"](data, "scripts/example")
    assert fixed.startswith(b"#!/usr/bin/env python3\n" + CHECKER["HEADER"])
    assert fixed.endswith(b"# Existing attribution\nprint('example')\r\n")
