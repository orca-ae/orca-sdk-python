"""Header names (and media types) are case-insensitive; the SDK carries headers as plain dicts
until `BaseClient._build_headers`, and `httpx.Headers` keeps and sends both entries of a dict that
holds two case-variants of one name, so every merge / lookup / `Omit()` before that point must fold case.
"""

from __future__ import annotations

from typing import Any, Type, Union, Iterator, cast
from unittest import mock

import httpx2 as httpx
import pytest

from orca import Orca, AsyncOrca
from orca._types import Omit
from orca._models import FinalRequestOptions
from orca._base_client import make_request_options

from .utils import update_env

base_url = "http://127.0.0.1:4010"
api_key = "my-orca-api-key"

ClientClass = Union[Type[Orca], Type[AsyncOrca]]

both_clients = pytest.mark.parametrize("client_cls", [Orca, AsyncOrca], ids=["sync", "async"])


def make_client(client_cls: ClientClass, **kwargs: Any) -> Orca | AsyncOrca:
    kwargs.setdefault("api_key", api_key)
    return client_cls(base_url=base_url, _strict_response_validation=True, **kwargs)


def build(client: Orca | AsyncOrca, **options: Any) -> httpx.Request:
    return client._build_request(FinalRequestOptions.construct(method="post", url="/foo", **options))


@pytest.fixture
def no_ambient_credentials() -> Iterator[None]:
    """No API key, auth token or credentials provider discoverable from the environment."""
    with mock.patch("orca._client.default_credentials", return_value=None):
        with update_env(
            ORCA_API_KEY=Omit(),
            ORCA_AUTH_TOKEN=Omit(),
        ):
            yield


class TestBuildHeaders:
    """SDK defaults < `default_headers` < `extra_headers`, whatever the casing."""

    @both_clients
    def test_default_headers_replace_sdk_header_case_insensitively(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, default_headers={"user-agent": "my-app/1.0"})

        request = build(client)

        assert request.headers.get_list("user-agent") == ["my-app/1.0"]

    @both_clients
    def test_default_headers_replace_client_subclass_header_case_insensitively(self, client_cls: ClientClass) -> None:
        # `orca-version` is added by the `Orca` subclass after the custom headers are spread in
        client = make_client(client_cls, default_headers={"Orca-Version": "2099-01-01"})

        request = build(client)

        assert request.headers.get_list("orca-version") == ["2099-01-01"]

    @both_clients
    def test_extra_headers_replace_default_headers_case_insensitively(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, default_headers={"X-Foo": "from-client"})

        request = build(client, **make_request_options(extra_headers={"x-foo": "from-request"}))

        assert request.headers.get_list("x-foo") == ["from-request"]

    @both_clients
    def test_extra_headers_replace_sdk_header_case_insensitively(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls)

        request = build(client, **make_request_options(extra_headers={"Orca-Version": "2099-01-01"}))

        assert request.headers.get_list("orca-version") == ["2099-01-01"]

    @both_clients
    def test_api_key_header_override_does_not_send_two_credentials(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, api_key="sk-client-key")

        request = build(client, **make_request_options(extra_headers={"x-api-key": "sk-request-key"}))

        assert request.headers.get_list("x-api-key") == ["sk-request-key"]

    @both_clients
    def test_authorization_default_header_does_not_send_two_credentials(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, api_key="client-key", default_headers={"authorization": "Bearer gateway"})

        request = build(client)

        assert request.headers.get_list("authorization") == ["Bearer gateway"]


class TestOmit:
    """`Omit()` removes a header whatever the casing."""

    @both_clients
    def test_extra_headers_omit_removes_default_header_case_insensitively(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, default_headers={"X-Foo": "bar"})

        request = build(client, **make_request_options(extra_headers={"x-foo": Omit()}))

        assert "x-foo" not in request.headers

    @both_clients
    def test_extra_headers_omit_removes_sdk_header_case_insensitively(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls)

        request = build(client, **make_request_options(extra_headers={"x-orca-client": Omit()}))

        assert "x-orca-client" not in request.headers

    @both_clients
    def test_default_headers_omit_removes_client_subclass_header_case_insensitively(
        self, client_cls: ClientClass
    ) -> None:
        client = make_client(client_cls, default_headers={"Orca-Version": Omit()})

        request = build(client)

        assert "orca-version" not in request.headers

    @both_clients
    def test_with_options_omit_removes_default_header_case_insensitively(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, default_headers={"X-Foo": "bar"}).with_options(
            default_headers=cast("dict[str, str]", {"x-foo": Omit()})
        )

        request = build(client)

        assert "x-foo" not in request.headers

    @both_clients
    def test_default_headers_omit_removes_per_request_sdk_header(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, default_headers={"X-Orca-Retry-Count": Omit()})

        request = build(client)

        assert "x-orca-retry-count" not in request.headers


class TestCopy:
    """`with_options(default_headers=...)` replaces the parent's header whatever the casing."""

    @both_clients
    def test_with_options_replaces_default_header_case_insensitively(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls, default_headers={"X-Foo": "parent"}).with_options(
            default_headers={"x-foo": "child"}
        )

        request = build(client)

        assert request.headers.get_list("x-foo") == ["child"]

    @both_clients
    def test_with_options_does_not_accumulate_case_variants(self, client_cls: ClientClass) -> None:
        client = (
            make_client(client_cls)
            .with_options(default_headers={"X-Foo": "one"})
            .with_options(default_headers={"x-foo": "two"})
            .with_options(default_headers={"X-FOO": "three"})
        )

        request = build(client)

        assert request.headers.get_list("x-foo") == ["three"]


class TestMultipartContentType:
    """A caller-supplied multipart `Content-Type` gets a boundary and the JSON body as form fields, whatever the casing."""

    @both_clients
    def test_lowercase_multipart_content_type(self, client_cls: ClientClass) -> None:
        client = make_client(client_cls)

        request = build(
            client,
            json_data={"purpose": "test"},
            files=[("file", ("hello.txt", b"hello", "text/plain"))],
            **make_request_options(extra_headers={"content-type": "multipart/form-data"}),
        )

        content_types = request.headers.get_list("content-type")
        assert len(content_types) == 1, content_types
        assert content_types[0].startswith("multipart/form-data; boundary=")
        assert b'name="purpose"' in request.read()

    def test_multipart_media_type_is_matched_case_insensitively(self) -> None:
        client = make_client(Orca)

        request = build(
            client,
            json_data={"purpose": "test"},
            files=[("file", ("hello.txt", b"hello", "text/plain"))],
            **make_request_options(extra_headers={"Content-Type": "Multipart/Form-Data"}),
        )

        content_types = request.headers.get_list("content-type")
        assert len(content_types) == 1, content_types
        assert "boundary=" in content_types[0]
        assert b'name="purpose"' in request.read()
