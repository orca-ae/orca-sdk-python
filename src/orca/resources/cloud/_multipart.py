"""Multipart encoding for cloud-extension request bodies.

Several cloud operations -- register/update a function, write function state,
trigger a function, upload a package -- declare their request body as
`multipart/form-data` whose parts mix plain scalars with *structured* values
(`functionConfig`, `updateOptions`, `state`, `metadata`).

A structured value has no form-scalar spelling. The contract carries each one as
a part of its own: a JSON document filed under the field's name, with filename
`{field}.json` and content type `application/json`. Servers on this API read the
part's declared content type, so getting the filename or type wrong is not
cosmetic -- the part is rejected.

`encode_cloud_multipart` performs that split once, so every cloud method that
sends multipart encodes it identically.
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Mapping, cast

from ..._files import is_file_content
from ..._types import FileTypes
from ..._utils import is_given, is_mapping, is_tuple_t, is_sequence
from ..._utils._json import openapi_dumps

__all__ = ["encode_cloud_multipart", "JSON_PART_CONTENT_TYPE"]

JSON_PART_CONTENT_TYPE = "application/json"


def encode_cloud_multipart(body: Mapping[str, object]) -> Tuple[Dict[str, object], List[Tuple[str, FileTypes]]]:
    """Split a cloud multipart body into its form fields and its file parts.

    Returns `(fields, files)`: `fields` are the scalars, ready to pass as the
    request body, and `files` are the parts httpx must encode as attachments --
    both caller-supplied uploads and the synthetic `{field}.json` documents that
    carry structured values.

    Pass the body through `transform` first: this reads part names straight off
    the mapping's keys, so they have to be the wire spellings the contract
    declares, not the snake_case argument names the methods take.

    Values that were never given are dropped, matching how omitted arguments are
    handled everywhere else.
    """
    fields: Dict[str, object] = {}
    files: List[Tuple[str, FileTypes]] = []

    for key, value in body.items():
        if not is_given(value):
            continue

        # File-ness is checked first: `bytes` is both file content and a
        # sequence, and here it always means "these are the bytes to upload".
        if is_file_content(value) or is_tuple_t(value):
            files.append((key, cast(FileTypes, value)))
        elif is_mapping(value) or (is_sequence(value) and not isinstance(value, str)):
            files.append((key, (f"{key}.json", openapi_dumps(value), JSON_PART_CONTENT_TYPE)))
        else:
            fields[key] = value

    return fields, files
