# Orca Python SDK

Python client for the [Orca Agent Engine](https://github.com/orca-ae/orca-managed-agents) API.

> **Status:** under construction. The client surface is being built out resource by resource.

## Installation

```sh
pip install orca-sdk
```

## Usage

```python
import os
from orca import Orca

client = Orca(
    api_key=os.environ.get("ORCA_API_KEY"),
    base_url=os.environ.get("ORCA_BASE_URL"),
)
```

`base_url` is the host root — the SDK appends `/v1/...` and `/apis/...` itself.

## License

Apache-2.0
