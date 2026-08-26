"""Packages served by the `cloud.sn.io` extension.

Wire field names are mirrored verbatim throughout the cloud namespace; see
`orca.types.cloud_package_metadata` for why.

`list`, `list_versions`, and `retrieve_metadata` have no declared response
schema in the contract, so they are typed as `object` -- the parsed body is
handed back untouched rather than forced into a shape the contract does not
promise.
"""

from __future__ import annotations

from typing import Dict

import httpx2

from ._gate import cloud_gate, async_cloud_gate
from ...types import cloud_package_upload_params, cloud_package_update_metadata_params
from ..._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from ..._utils import (
    transform,
    path_template,
    async_transform,
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ._multipart import encode_cloud_multipart
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.cloud_package_metadata import CloudPackageMetadataParam

__all__ = ["Packages", "AsyncPackages"]


class Packages(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PackagesWithRawResponse:
        return PackagesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PackagesWithStreamingResponse:
        return PackagesWithStreamingResponse(self)

    def list(
        self,
        type: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        List the packages of one package type.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          type: The package type to list, for example `function` or `sink`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/packages/{type}", type=type),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def list_versions(
        self,
        type: str,
        package_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        List the stored versions of one package.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package whose versions are listed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/packages/{type}/{package_name}", type=type, package_name=package_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def download(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> httpx2.Response:
        """
        Download the bytes of one package version.

        This serves the package archive rather than a document, so it returns the
        underlying HTTP response: read `.content`, or stream it yourself.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to download.

          version: The version to download.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._get(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}",
                type=type,
                package_name=package_name,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx2.Response,
        )

    def upload(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        metadata: CloudPackageMetadataParam | Omit = omit,
        file: FileTypes | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Upload one package version.

        The body is `multipart/form-data`. `metadata` is a structured value, so it
        travels as its own JSON part rather than as form scalars; `_multipart.py`
        explains the encoding. The contract declares no response schema, so the
        parsed body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to upload under.

          version: The version to create.

          metadata: Descriptive metadata stored alongside the bytes.

          file: The package bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            transform({"metadata": metadata, "file": file}, cloud_package_upload_params.CloudPackageUploadParams)
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}",
                type=type,
                package_name=package_name,
                version=version,
            ),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def delete(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Permanently delete one package version.

        There is no archive for packages. The contract declares no response schema,
        so the parsed body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to delete a version of.

          version: The version to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._delete(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}",
                type=type,
                package_name=package_name,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve_metadata(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Retrieve the metadata stored with one package version.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to describe.

          version: The version to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._get(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}/metadata",
                type=type,
                package_name=package_name,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def update_metadata(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        description: str | Omit = omit,
        contact: str | Omit = omit,
        create_time: int | Omit = omit,
        modification_time: int | Omit = omit,
        properties: Dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Replace the metadata stored with one package version.

        This is a `PUT` and the body is JSON, not multipart: the metadata document
        replaces the stored one rather than merging into it, so send every field you
        want to keep. The contract declares no response schema, so the parsed body
        is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to update.

          version: The version to update.

          description: Free-text description of the package.

          contact: Who to contact about this package.

          create_time: Epoch milliseconds, per the contract's int64 timestamps. Sent as `createTime`.

          modification_time: Epoch milliseconds, per the contract's int64 timestamps. Sent as
              `modificationTime`.

          properties: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._put(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}/metadata",
                type=type,
                package_name=package_name,
                version=version,
            ),
            body=maybe_transform(
                {
                    "description": description,
                    "contact": contact,
                    "create_time": create_time,
                    "modification_time": modification_time,
                    "properties": properties,
                },
                cloud_package_update_metadata_params.CloudPackageUpdateMetadataParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncPackages(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPackagesWithRawResponse:
        return AsyncPackagesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPackagesWithStreamingResponse:
        return AsyncPackagesWithStreamingResponse(self)

    async def list(
        self,
        type: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        List the packages of one package type.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          type: The package type to list, for example `function` or `sink`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/packages/{type}", type=type),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def list_versions(
        self,
        type: str,
        package_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        List the stored versions of one package.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package whose versions are listed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/packages/{type}/{package_name}", type=type, package_name=package_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def download(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> httpx2.Response:
        """
        Download the bytes of one package version.

        This serves the package archive rather than a document, so it returns the
        underlying HTTP response: read `.content`, or stream it yourself.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to download.

          version: The version to download.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._get(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}",
                type=type,
                package_name=package_name,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx2.Response,
        )

    async def upload(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        metadata: CloudPackageMetadataParam | Omit = omit,
        file: FileTypes | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Upload one package version.

        The body is `multipart/form-data`. `metadata` is a structured value, so it
        travels as its own JSON part rather than as form scalars; `_multipart.py`
        explains the encoding. The contract declares no response schema, so the
        parsed body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to upload under.

          version: The version to create.

          metadata: Descriptive metadata stored alongside the bytes.

          file: The package bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            await async_transform(
                {"metadata": metadata, "file": file}, cloud_package_upload_params.CloudPackageUploadParams
            )
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}",
                type=type,
                package_name=package_name,
                version=version,
            ),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def delete(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Permanently delete one package version.

        There is no archive for packages. The contract declares no response schema,
        so the parsed body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to delete a version of.

          version: The version to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._delete(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}",
                type=type,
                package_name=package_name,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve_metadata(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Retrieve the metadata stored with one package version.

        The contract declares no response schema for this operation, so the parsed
        body is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to describe.

          version: The version to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._get(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}/metadata",
                type=type,
                package_name=package_name,
                version=version,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def update_metadata(
        self,
        type: str,
        package_name: str,
        version: str,
        *,
        description: str | Omit = omit,
        contact: str | Omit = omit,
        create_time: int | Omit = omit,
        modification_time: int | Omit = omit,
        properties: Dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Replace the metadata stored with one package version.

        This is a `PUT` and the body is JSON, not multipart: the metadata document
        replaces the stored one rather than merging into it, so send every field you
        want to keep. The contract declares no response schema, so the parsed body
        is returned as-is.

        Args:
          type: The package type, for example `function` or `sink`.

          package_name: The package to update.

          version: The version to update.

          description: Free-text description of the package.

          contact: Who to contact about this package.

          create_time: Epoch milliseconds, per the contract's int64 timestamps. Sent as `createTime`.

          modification_time: Epoch milliseconds, per the contract's int64 timestamps. Sent as
              `modificationTime`.

          properties: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        if not package_name:
            raise ValueError(f"Expected a non-empty value for `package_name` but received {package_name!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._put(
            path_template(
                "/apis/cloud.sn.io/v1/packages/{type}/{package_name}/{version}/metadata",
                type=type,
                package_name=package_name,
                version=version,
            ),
            body=await async_maybe_transform(
                {
                    "description": description,
                    "contact": contact,
                    "create_time": create_time,
                    "modification_time": modification_time,
                    "properties": properties,
                },
                cloud_package_update_metadata_params.CloudPackageUpdateMetadataParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class PackagesWithRawResponse:
    def __init__(self, packages: Packages) -> None:
        self._packages = packages

        self.list = to_raw_response_wrapper(packages.list)
        self.list_versions = to_raw_response_wrapper(packages.list_versions)
        self.download = to_raw_response_wrapper(packages.download)
        self.upload = to_raw_response_wrapper(packages.upload)
        self.delete = to_raw_response_wrapper(packages.delete)
        self.retrieve_metadata = to_raw_response_wrapper(packages.retrieve_metadata)
        self.update_metadata = to_raw_response_wrapper(packages.update_metadata)


class AsyncPackagesWithRawResponse:
    def __init__(self, packages: AsyncPackages) -> None:
        self._packages = packages

        self.list = async_to_raw_response_wrapper(packages.list)
        self.list_versions = async_to_raw_response_wrapper(packages.list_versions)
        self.download = async_to_raw_response_wrapper(packages.download)
        self.upload = async_to_raw_response_wrapper(packages.upload)
        self.delete = async_to_raw_response_wrapper(packages.delete)
        self.retrieve_metadata = async_to_raw_response_wrapper(packages.retrieve_metadata)
        self.update_metadata = async_to_raw_response_wrapper(packages.update_metadata)


class PackagesWithStreamingResponse:
    def __init__(self, packages: Packages) -> None:
        self._packages = packages

        self.list = to_streamed_response_wrapper(packages.list)
        self.list_versions = to_streamed_response_wrapper(packages.list_versions)
        self.download = to_streamed_response_wrapper(packages.download)
        self.upload = to_streamed_response_wrapper(packages.upload)
        self.delete = to_streamed_response_wrapper(packages.delete)
        self.retrieve_metadata = to_streamed_response_wrapper(packages.retrieve_metadata)
        self.update_metadata = to_streamed_response_wrapper(packages.update_metadata)


class AsyncPackagesWithStreamingResponse:
    def __init__(self, packages: AsyncPackages) -> None:
        self._packages = packages

        self.list = async_to_streamed_response_wrapper(packages.list)
        self.list_versions = async_to_streamed_response_wrapper(packages.list_versions)
        self.download = async_to_streamed_response_wrapper(packages.download)
        self.upload = async_to_streamed_response_wrapper(packages.upload)
        self.delete = async_to_streamed_response_wrapper(packages.delete)
        self.retrieve_metadata = async_to_streamed_response_wrapper(packages.retrieve_metadata)
        self.update_metadata = async_to_streamed_response_wrapper(packages.update_metadata)
