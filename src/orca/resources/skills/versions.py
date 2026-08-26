from __future__ import annotations

from typing import Mapping, cast

import httpx2

from ...types import skill_version_list_params, skill_version_create_params
from ..._types import Body, Omit, Query, Headers, NotGiven, FileTypes, SequenceNotStr, omit, not_given
from ..._utils import extract_files, path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.skill_version import SkillVersion, DeletedSkillVersion

__all__ = ["Versions", "AsyncVersions"]


class Versions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VersionsWithRawResponse:
        return VersionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VersionsWithStreamingResponse:
        return VersionsWithStreamingResponse(self)

    def create(
        self,
        skill_id: str,
        *,
        files: SequenceNotStr[FileTypes],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Create a new version of a skill from an uploaded bundle.

        Sent as `multipart/form-data`. A version is always a complete bundle, never a
        patch against the previous one, so `files` must carry every file the version
        needs.

        Args:
          skill_id: The skill to add a version to.

          files: The skill bundle files for the new version.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        body = {"files": files}
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It is required to explicitly set the content type so the server parses the parts.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            body=maybe_transform(body, skill_version_create_params.SkillVersionCreateParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    def retrieve(
        self,
        skill_id: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Retrieve one version of a skill.

        Args:
          skill_id: The skill the version belongs to.

          version: The version string, as carried by `SkillVersion.version`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._get(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    def list(
        self,
        skill_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[SkillVersion]:
        """
        List the versions of a skill.

        Args:
          skill_id: The skill whose versions to list.

          limit: Maximum number of versions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return self._get_api_list(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            page=SyncPageCursor[SkillVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    skill_version_list_params.SkillVersionListParams,
                ),
            ),
            model=SkillVersion,
        )

    def delete(
        self,
        skill_id: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSkillVersion:
        """
        Permanently delete one version of a skill.

        This is a delete, not an archive: the version is gone and its content can no
        longer be fetched. The returned tombstone identifies the version by number.

        Args:
          skill_id: The skill the version belongs to.

          version: The version string, as carried by `SkillVersion.version`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return self._delete(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSkillVersion,
        )


class AsyncVersions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersionsWithRawResponse:
        return AsyncVersionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersionsWithStreamingResponse:
        return AsyncVersionsWithStreamingResponse(self)

    async def create(
        self,
        skill_id: str,
        *,
        files: SequenceNotStr[FileTypes],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Create a new version of a skill from an uploaded bundle.

        Sent as `multipart/form-data`. A version is always a complete bundle, never a
        patch against the previous one, so `files` must carry every file the version
        needs.

        Args:
          skill_id: The skill to add a version to.

          files: The skill bundle files for the new version.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        body = {"files": files}
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It is required to explicitly set the content type so the server parses the parts.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            body=await async_maybe_transform(body, skill_version_create_params.SkillVersionCreateParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    async def retrieve(
        self,
        skill_id: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SkillVersion:
        """
        Retrieve one version of a skill.

        Args:
          skill_id: The skill the version belongs to.

          version: The version string, as carried by `SkillVersion.version`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._get(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkillVersion,
        )

    def list(
        self,
        skill_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SkillVersion, AsyncPageCursor[SkillVersion]]:
        """
        List the versions of a skill.

        Args:
          skill_id: The skill whose versions to list.

          limit: Maximum number of versions to return per page.

          page: Opaque page token from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        return self._get_api_list(
            path_template("/v1/skills/{skill_id}/versions", skill_id=skill_id),
            page=AsyncPageCursor[SkillVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page},
                    skill_version_list_params.SkillVersionListParams,
                ),
            ),
            model=SkillVersion,
        )

    async def delete(
        self,
        skill_id: str,
        version: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSkillVersion:
        """
        Permanently delete one version of a skill.

        This is a delete, not an archive: the version is gone and its content can no
        longer be fetched. The returned tombstone identifies the version by number.

        Args:
          skill_id: The skill the version belongs to.

          version: The version string, as carried by `SkillVersion.version`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not skill_id:
            raise ValueError(f"Expected a non-empty value for `skill_id` but received {skill_id!r}")
        if not version:
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        return await self._delete(
            path_template("/v1/skills/{skill_id}/versions/{version}", skill_id=skill_id, version=version),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSkillVersion,
        )


class VersionsWithRawResponse:
    def __init__(self, versions: Versions) -> None:
        self._versions = versions

        self.create = to_raw_response_wrapper(versions.create)
        self.retrieve = to_raw_response_wrapper(versions.retrieve)
        self.list = to_raw_response_wrapper(versions.list)
        self.delete = to_raw_response_wrapper(versions.delete)


class AsyncVersionsWithRawResponse:
    def __init__(self, versions: AsyncVersions) -> None:
        self._versions = versions

        self.create = async_to_raw_response_wrapper(versions.create)
        self.retrieve = async_to_raw_response_wrapper(versions.retrieve)
        self.list = async_to_raw_response_wrapper(versions.list)
        self.delete = async_to_raw_response_wrapper(versions.delete)


class VersionsWithStreamingResponse:
    def __init__(self, versions: Versions) -> None:
        self._versions = versions

        self.create = to_streamed_response_wrapper(versions.create)
        self.retrieve = to_streamed_response_wrapper(versions.retrieve)
        self.list = to_streamed_response_wrapper(versions.list)
        self.delete = to_streamed_response_wrapper(versions.delete)


class AsyncVersionsWithStreamingResponse:
    def __init__(self, versions: AsyncVersions) -> None:
        self._versions = versions

        self.create = async_to_streamed_response_wrapper(versions.create)
        self.retrieve = async_to_streamed_response_wrapper(versions.retrieve)
        self.list = async_to_streamed_response_wrapper(versions.list)
        self.delete = async_to_streamed_response_wrapper(versions.delete)
