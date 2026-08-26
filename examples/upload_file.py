#!/usr/bin/env python
"""Upload a file, list files, then delete the upload.

Run with ORCA_BASE_URL and ORCA_API_KEY set.
"""

from __future__ import annotations

import sys

from orca import Orca, OrcaError


def main() -> None:
    client = Orca()

    metadata = client.files.upload(file=("demo.txt", b"hello\n", "text/plain"))
    print(f"uploaded: {metadata.id}")

    print("first few files:")
    for index, existing in enumerate(client.files.list()):
        print(f"  {existing.id}")
        if index >= 4:
            break

    client.files.delete(metadata.id)
    print(f"deleted {metadata.id}")


if __name__ == "__main__":
    try:
        main()
    except OrcaError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(1) from err
