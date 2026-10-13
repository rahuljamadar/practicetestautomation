from __future__ import annotations

import asyncio

from fastmcp import Client

from skillfinder_mcp import server


REQUIRED_TOOLS = {
    "list_skills",
    "search_skills",
    "get_skill",
    "get_skill_file",
    "list_skill_files",
}


def _discover() -> tuple[list, list, list, list]:
    async def run() -> tuple[list, list, list, list]:
        async with Client(server.mcp) as client:
            return (
                await client.list_tools(),
                await client.list_resources(),
                await client.list_resource_templates(),
                await client.list_prompts(),
            )

    return asyncio.run(run())


def test_read_only_surface_matches_screenshot_tools() -> None:
    tools, resources, templates, prompts = _discover()

    names = {tool.name for tool in tools}
    assert REQUIRED_TOOLS <= names
    assert "sync_skills" not in names  # write tool hidden by default
    assert len(resources) == 3
    assert len(templates) == 2
    assert {prompt.name for prompt in prompts} == {
        "find_skill",
        "use_skill",
        "plan_skills_for_project",
    }


def test_search_tool_finds_playwright_api() -> None:
    async def run() -> dict:
        async with Client(server.mcp) as client:
            return await client.call_tool("search_skills", {"query": "playwright api"})

    result = asyncio.run(run())
    payload = result.data

    assert payload["total_matches"] >= 1
    assert payload["results"][0]["name"] == "pw-api-tester"


def test_catalog_resource_exposes_all_skills() -> None:
    async def run() -> dict:
        async with Client(server.mcp) as client:
            return await client.call_tool("skills_summary", {})

    summary = asyncio.run(run()).data

    assert summary["total_skills"] >= 50
    assert summary["malformed"] == []


def test_write_tool_requires_explicit_enablement() -> None:
    server.mcp.enable(tags={"write"}, components={"tool"})
    try:
        tools, _, _, _ = _discover()
        names = {tool.name for tool in tools}
        assert "sync_skills" in names
    finally:
        server.mcp.disable(tags={"write"}, components={"tool"})


def test_auth_is_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("SKILLFINDER_AUTH_TOKEN", raising=False)
    assert server._build_auth() is None


def test_auth_is_enabled_when_token_env_is_set(monkeypatch) -> None:
    monkeypatch.setenv("SKILLFINDER_AUTH_TOKEN", "team-secret")
    assert server._build_auth() is not None
