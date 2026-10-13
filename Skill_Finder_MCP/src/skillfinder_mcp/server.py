"""FastMCP server exposing the skill catalog as tools, resources and prompts."""

from __future__ import annotations

import argparse
import json
import os
import socket
from pathlib import Path

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse

from skillfinder_mcp import sync as skill_sync
from skillfinder_mcp.catalog import DEFAULT_LIMIT, MAX_LIMIT, SkillCatalog


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = Path(
    os.environ.get("SKILLFINDER_SKILLS_DIR", PROJECT_ROOT / "skills")
).expanduser()
CATALOG = SkillCatalog(SKILLS_DIR)


def _build_auth():
    """Return a static bearer-token verifier when SKILLFINDER_AUTH_TOKEN is set.

    Unset (the default) means no authentication — suitable only for loopback or a
    trusted network. Setting the env var requires every client to send
    ``Authorization: Bearer <token>``.
    """
    token = os.environ.get("SKILLFINDER_AUTH_TOKEN", "").strip()
    if not token:
        return None
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

    return StaticTokenVerifier(tokens={token: {"client_id": "qa-team", "scopes": []}})


def _lan_ip() -> str:
    """Best-effort LAN IP for share URLs (falls back to loopback)."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("8.8.8.8", 80))
        return probe.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        probe.close()


mcp = FastMCP("testskill-finder", auth=_build_auth())


@mcp.custom_route("/", methods=["GET"], include_in_schema=False)
async def browser_help(request: Request) -> HTMLResponse:
    del request
    return HTMLResponse(
        """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>testskill-finder MCP</title><body style="font:16px system-ui;max-width:720px;margin:12vh auto;padding:24px;color:#18212b">
<h1>testskill-finder MCP</h1><p>This is an MCP endpoint, not a regular website.</p>
<p>Connect an MCP client or open MCP Inspector and use the Streamable HTTP URL:</p>
<p><code>http://127.0.0.1:8000/mcp</code></p>
<p>Try a search for "playwright api", "test case", "test plan" or "bug".</p>
</body></html>"""
    )


# ----------------------------------------------------------------------------- tools
@mcp.tool(description="List skills in the catalog, optionally filtered by category or framework pack.")
def list_skills(
    category: str | None = None, pack: str | None = None, limit: int = DEFAULT_LIMIT
) -> dict:
    return CATALOG.list_skills(category=category, pack=pack, limit=limit)


@mcp.tool(description="Search skills by keyword across name, description and body (e.g. 'playwright api').")
def search_skills(
    query: str,
    category: str | None = None,
    pack: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> dict:
    return CATALOG.rank(query, category=category, pack=pack, limit=limit)


@mcp.tool(description="Return the full SKILL.md content and metadata for one skill by name.")
def get_skill(name: str) -> dict:
    return CATALOG.get_skill(name)


@mcp.tool(description="Read a single file bundled in a skill folder (e.g. 'references/checklist.md').")
def get_skill_file(name: str, file: str) -> dict:
    return CATALOG.get_skill_file(name, file)


@mcp.tool(description="List every file bundled in a skill folder.")
def list_skill_files(name: str) -> dict:
    return CATALOG.list_skill_files(name)


@mcp.tool(description="Report catalog health: total skills, categories, packs and malformed files.")
def skills_summary() -> dict:
    return CATALOG.summary()


@mcp.tool(description="List all categories and framework packs with their member skills.")
def list_categories() -> dict:
    return CATALOG.list_categories()


@mcp.tool(description="Structured browse of skills by category, framework pack and/or STLC phase.")
def filter_skills(
    category: str | None = None,
    pack: str | None = None,
    phase: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> dict:
    return CATALOG.filter_skills(category=category, pack=pack, phase=phase, limit=limit)


@mcp.tool(description="Return only the frontmatter metadata for one skill.")
def get_skill_metadata(name: str) -> dict:
    return CATALOG.get_skill_metadata(name)


@mcp.tool(description="Search text inside a single skill's files, returning matching lines.")
def search_in_skill(name: str, query: str, limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.search_in_skill(name, query, limit=limit)


@mcp.tool(description="Recommend the best-fitting skills for a free-text task description.")
def recommend_skills(task: str, limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.recommend(task, limit=limit)


@mcp.tool(
    tags={"write"},
    description="Download/refresh skills from the upstream GitHub repo into the local skills folder.",
)
def sync_skills(dry_run: bool = False) -> dict:
    report = skill_sync.sync_skills(SKILLS_DIR, dry_run=dry_run)
    if not dry_run and not report["errors"]:
        CATALOG.refresh()
    report["catalog_total"] = len(CATALOG.skills)
    return report


mcp.disable(tags={"write"}, components={"tool"})


# ------------------------------------------------------------------------- resources
@mcp.resource("skills://index", description="JSON index of all skills in the catalog.")
def skills_index_resource() -> list[dict]:
    return CATALOG.index()


@mcp.resource("skills://categories", description="Categories and framework packs with member skills.")
def skills_categories_resource() -> dict:
    return CATALOG.list_categories()


@mcp.resource("skills://summary", description="Catalog totals and health.")
def skills_summary_resource() -> dict:
    return CATALOG.summary()


@mcp.resource("skills://skill/{name}", description="Full SKILL.md markdown for one skill.")
def skill_content_resource(name: str) -> str:
    return CATALOG.get_skill(name)["content"]


@mcp.resource("skills://skill/{name}/files", description="File listing for one skill.")
def skill_files_resource(name: str) -> dict:
    return CATALOG.list_skill_files(name)


# --------------------------------------------------------------------------- prompts
@mcp.prompt(description="Find the best skill(s) for a task using the catalog.")
def find_skill(task: str) -> str:
    return (
        "Use the testskill-finder MCP to locate the most relevant QA agent skill for the "
        "task below. Call search_skills (and recommend_skills if useful), then pick the "
        "single best skill by name. Explain in one or two sentences why it fits, and cite "
        "the skill name and its category. If nothing matches well, say so and list the "
        f"closest candidates.\n\nTask: {task}"
    )


@mcp.prompt(description="Load a chosen skill as operating instructions for a task.")
def use_skill(skill_name: str, task: str = "") -> str:
    skill = CATALOG.get_skill(skill_name)
    header = (
        f"Follow the '{skill['name']}' skill from the testskill-finder catalog for this task."
        + (f"\n\nTask: {task}" if task else "")
    )
    return f"{header}\n\n--- SKILL: {skill['name']} ---\n\n{skill['content']}"


@mcp.prompt(description="Assemble a set of skills across the STLC for a project.")
def plan_skills_for_project(project: str) -> str:
    return (
        "Plan which testskill-finder skills to apply across the software testing life cycle "
        "for the project below. Search the catalog (list_categories, filter_skills, "
        "search_skills) and propose an ordered set of skills by STLC phase "
        "(requirement -> plan -> design -> cases -> execute -> defects -> closure), naming "
        "each skill and what it contributes. Do not invent skills; only cite catalog names.\n\n"
        f"Project: {project}"
    )


def _print_share_config(arguments: argparse.Namespace) -> None:
    """Print the reachable URL and a ready-to-paste MCP client config snippet."""
    host = _lan_ip() if arguments.host in ("0.0.0.0", "::") else arguments.host
    url = f"http://{host}:{arguments.port}{arguments.path}"
    client: dict[str, object] = {"type": "http", "url": url}
    if os.environ.get("SKILLFINDER_AUTH_TOKEN", "").strip():
        client["headers"] = {"Authorization": "Bearer <your-shared-token>"}
    print(f"Share URL: {url}")
    print(f"Browser help page: http://{host}:{arguments.port}/")
    print("Add this to each teammate's MCP client config (.mcp.json):")
    print(json.dumps({"mcpServers": {"testskill-finder": client}}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the testskill-finder MCP server")
    parser.add_argument("--transport", choices=("stdio", "http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--path", default="/mcp")
    parser.add_argument(
        "--enable-write-tools",
        action="store_true",
        help="Expose the sync_skills tool that downloads skills from the upstream repo.",
    )
    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print the share URL and a client config snippet, then exit.",
    )
    arguments = parser.parse_args()

    if arguments.print_config:
        _print_share_config(arguments)
        return

    if arguments.enable_write_tools:
        mcp.enable(tags={"write"}, components={"tool"})

    if arguments.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(
            transport="http",
            host=arguments.host,
            port=arguments.port,
            path=arguments.path,
            stateless_http=True,
        )


if __name__ == "__main__":
    main()
