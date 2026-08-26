from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca
from tests.utils import assert_matches_type
from orca.pagination import SyncPageCursor, AsyncPageCursor
from orca.types.skill import Skill, DeletedSkill
from orca.types.skill_version import SkillVersion, DeletedSkillVersion

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

SKILL: dict[str, Any] = {
    "id": "skill_123",
    "type": "skill",
    "display_title": "Demo skill",
    "latest_version": "1",
    "source": "custom",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}

DELETED_SKILL: dict[str, Any] = {"id": "skill_123", "type": "skill_deleted"}

SKILL_VERSION: dict[str, Any] = {
    "id": "skillver_123",
    "type": "skill_version",
    "skill_id": "skill_123",
    "name": "demo",
    "description": "a demo skill",
    "directory": "demo",
    "version": "1",
    "created_at": "2026-01-01T00:00:00Z",
}

DELETED_SKILL_VERSION: dict[str, Any] = {"id": "1", "type": "skill_version_deleted"}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*skills: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(skills), "next_page": next_page}


class TestSkills:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        skill = client.skills.create(files=[("SKILL.md", b"# demo")])
        assert_matches_type(Skill, skill, path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_sends_multipart(self, client: Orca, respx_mock: MockRouter) -> None:
        """The bundle is uploaded as form parts, not as a JSON body."""
        route = respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        client.skills.create(files=[("SKILL.md", b"# demo"), ("run.py", b"print()")], display_title="Demo skill")

        request = _req(route)
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        content = request.content
        assert content.count(b'name="files[]"') == 2
        assert b'filename="SKILL.md"' in content
        assert b'filename="run.py"' in content
        assert b'name="display_title"' in content
        assert b"Demo skill" in content

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_omits_absent_display_title(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        client.skills.create(files=[b"bundle"])
        assert b'name="display_title"' not in _req(route).content

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        response = client.skills.with_raw_response.create(files=[b"bundle"])
        assert response.is_closed is True
        assert_matches_type(Skill, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        with client.skills.with_streaming_response.create(files=[b"bundle"]) as response:
            assert not response.is_closed
            assert_matches_type(Skill, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/skills/skill_123").mock(return_value=httpx2.Response(200, json=SKILL))
        assert_matches_type(Skill, client.skills.retrieve("skill_123"), path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.skills.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=SKILL))
        client.skills.retrieve("a b/c")
        assert "/v1/skills/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/skills").mock(return_value=httpx2.Response(200, json=_page(SKILL)))
        assert_matches_type(SyncPageCursor[Skill], client.skills.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/skills").mock(return_value=httpx2.Response(200, json=_page(SKILL)))
        client.skills.list(limit=20, page="tok")
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["page"] == "tok"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**SKILL, "id": "skill_456"}
        respx_mock.get("/v1/skills").mock(
            side_effect=[
                httpx2.Response(200, json=_page(SKILL, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [s.id for s in client.skills.list()] == ["skill_123", "skill_456"]
        assert _req(respx_mock, 1).url.params["page"] == "cursor-2"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/skills/skill_123").mock(return_value=httpx2.Response(200, json=DELETED_SKILL))
        assert_matches_type(DeletedSkill, client.skills.delete("skill_123"), path=["response"])
        assert _req(route).method == "DELETE"

    @parametrize
    def test_path_params_delete(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.skills.with_raw_response.delete("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/skills").mock(return_value=httpx2.Response(200, json=_page()))
        client.skills.list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_versions_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/skills/skill_123/versions").mock(
            return_value=httpx2.Response(200, json=SKILL_VERSION)
        )
        version = client.skills.versions.create("skill_123", files=[("SKILL.md", b"# demo")])
        assert_matches_type(SkillVersion, version, path=["response"])

        request = _req(route)
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        assert b'name="files[]"' in request.content

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_versions_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/skills/skill_123/versions/1").mock(return_value=httpx2.Response(200, json=SKILL_VERSION))
        assert_matches_type(SkillVersion, client.skills.versions.retrieve("skill_123", "1"), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_versions_list(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/skills/skill_123/versions").mock(
            return_value=httpx2.Response(200, json=_page(SKILL_VERSION))
        )
        assert_matches_type(
            SyncPageCursor[SkillVersion], client.skills.versions.list("skill_123", limit=5), path=["response"]
        )
        assert _req(route).url.params["limit"] == "5"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_versions_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/skills/skill_123/versions/1").mock(
            return_value=httpx2.Response(200, json=DELETED_SKILL_VERSION)
        )
        assert_matches_type(DeletedSkillVersion, client.skills.versions.delete("skill_123", "1"), path=["response"])
        assert _req(route).method == "DELETE"

    @parametrize
    def test_versions_path_params(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.skills.versions.with_raw_response.list("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.skills.versions.with_raw_response.create("", files=[b"bundle"])
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            client.skills.versions.with_raw_response.retrieve("skill_123", "")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            client.skills.versions.with_raw_response.delete("skill_123", "")


class TestAsyncSkills:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        skill = await async_client.skills.create(files=[("SKILL.md", b"# demo")], display_title="Demo skill")
        assert_matches_type(Skill, skill, path=["response"])

        request = _req(route)
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        assert b'name="files[]"' in request.content

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        response = await async_client.skills.with_raw_response.create(files=[b"bundle"])
        assert response.is_closed is True
        assert_matches_type(Skill, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/skills").mock(return_value=httpx2.Response(200, json=SKILL))
        async with async_client.skills.with_streaming_response.create(files=[b"bundle"]) as response:
            assert not response.is_closed
            assert_matches_type(Skill, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/skills/skill_123").mock(return_value=httpx2.Response(200, json=SKILL))
        assert_matches_type(Skill, await async_client.skills.retrieve("skill_123"), path=["response"])

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            await async_client.skills.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/skills").mock(return_value=httpx2.Response(200, json=_page(SKILL)))
        assert_matches_type(AsyncPageCursor[Skill], await async_client.skills.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**SKILL, "id": "skill_456"}
        respx_mock.get("/v1/skills").mock(
            side_effect=[
                httpx2.Response(200, json=_page(SKILL, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [s.id async for s in async_client.skills.list()] == ["skill_123", "skill_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/skills/skill_123").mock(return_value=httpx2.Response(200, json=DELETED_SKILL))
        assert_matches_type(DeletedSkill, await async_client.skills.delete("skill_123"), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_versions_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/skills/skill_123/versions").mock(return_value=httpx2.Response(200, json=SKILL_VERSION))
        version = await async_client.skills.versions.create("skill_123", files=[b"bundle"])
        assert_matches_type(SkillVersion, version, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_versions_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/skills/skill_123/versions/1").mock(return_value=httpx2.Response(200, json=SKILL_VERSION))
        assert_matches_type(
            SkillVersion, await async_client.skills.versions.retrieve("skill_123", "1"), path=["response"]
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_versions_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/skills/skill_123/versions").mock(
            return_value=httpx2.Response(200, json=_page(SKILL_VERSION))
        )
        assert_matches_type(
            AsyncPageCursor[SkillVersion], await async_client.skills.versions.list("skill_123"), path=["response"]
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_versions_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/skills/skill_123/versions/1").mock(
            return_value=httpx2.Response(200, json=DELETED_SKILL_VERSION)
        )
        assert_matches_type(
            DeletedSkillVersion, await async_client.skills.versions.delete("skill_123", "1"), path=["response"]
        )
