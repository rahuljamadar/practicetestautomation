# testskill-finder MCP

A **local-first MCP server** that lets any LLM discover, search and read QA *agent
skills* by keyword. Ask it for "Playwright", "Playwright API", "test case creator",
"test plan", "bug strategy" — it finds the right skill and hands back the full
instructions.

The **single source of truth is the [`skills/`](./skills) folder**: every
sub-directory that contains a `SKILL.md` is one discoverable skill. The catalog ships
with **50 skills**.

- **36 skills** are vendored verbatim from
  [`PramodDutta/skillmasterclass`](https://github.com/PramodDutta/skillmasterclass)
  (via [`scripts/sync_skills.py`](./scripts/sync_skills.py)).
- **14 skills** are authored locally in the same `SKILL.md` format under
  `08-non-functional/`, `09-strategy-and-management/` and `10-specialized/`.

The MCP server is built with [FastMCP](https://gofastmcp.com) and speaks **stdio**
(for LLM clients) and **streamable HTTP** (for remote clients and MCP Inspector).

## Layout

```
Skill_Finder_MCP/
├── skills/                     # SOURCE OF TRUTH — 50 skill folders
│   ├── 01-requirement-analysis/ … 07-test-closure/   # STLC phase skills
│   ├── framework-packs/
│   │   ├── playwright-pack/pw-*/
│   │   └── selenium-pack/se-*/
│   ├── 08-non-functional/       # authored
│   ├── 09-strategy-and-management/  # authored
│   └── 10-specialized/          # authored
├── src/skillfinder_mcp/
│   ├── catalog.py   # scan skills/, parse frontmatter, search / rank / read
│   ├── sync.py      # download upstream skills
│   └── server.py    # FastMCP("testskill-finder") — tools, resources, prompts, CLI
├── scripts/
│   ├── sync_skills.py
│   └── start_skillfinder_mcp.ps1
└── tests/
```

## Quickstart

```powershell
cd Skill_Finder_MCP
uv sync --all-extras                 # create .venv, install fastmcp + pyyaml + pytest
uv run python scripts/sync_skills.py # (re)download the 36 upstream skills into skills/
uv run pytest -q                     # run the test suite
```

### Run the server (stdio — for LLM clients)

```powershell
uv run skillfinder-mcp
```

### Run the server (streamable HTTP — for Inspector / remote LLMs)

```powershell
uv run skillfinder-mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp
```

Then open **MCP Inspector** at the endpoint `http://127.0.0.1:8000/mcp`:

```powershell
npx @modelcontextprotocol/inspector@2.10.1 --transport http --server-url http://127.0.0.1:8000/mcp
```

Or use the bundled launcher, which starts the HTTP server and launches Inspector:

```powershell
./scripts/start_skillfinder_mcp.ps1
```

The server reports its name as **`testskill-finder`**.

## MCP surface

### Tools

| Tool | Description |
| --- | --- |
| `list_skills(category?, pack?, limit?)` | List skills, optionally filtered by category or framework pack. |
| `search_skills(query, category?, pack?, limit?)` | Keyword search across skill name, description and body. |
| `get_skill(name)` | Full `SKILL.md` content plus metadata for one skill. |
| `get_skill_file(name, file)` | Read a single file inside a skill folder (e.g. `references/…`). |
| `list_skill_files(name)` | List every file bundled in a skill folder. |
| `skills_summary()` | Totals by category and pack, plus malformed-file report. |
| `list_categories()` | Categories and packs with their member skills. |
| `filter_skills(category?, pack?, phase?, limit?)` | Structured browse by category / pack / STLC phase. |
| `get_skill_metadata(name)` | Frontmatter only. |
| `search_in_skill(name, query, limit?)` | Search text inside one skill's files, with line hits. |
| `recommend_skills(task, limit?)` | Rank the best-fitting skills for a free-text task. |
| `sync_skills(dry_run?)` | *(write, hidden by default)* Download/refresh upstream skills. |

`sync_skills` is tagged `write` and hidden unless the server is started with
`--enable-write-tools`.

### Resources

| URI | Description |
| --- | --- |
| `skills://index` | JSON index of all skills (name, category, pack, description). |
| `skills://categories` | Categories and packs with member skills. |
| `skills://summary` | Catalog totals and health. |
| `skills://skill/{name}` | Full markdown of a single skill. |
| `skills://skill/{name}/files` | File listing for a single skill. |

### Prompts

| Prompt | Description |
| --- | --- |
| `find_skill(task)` | Instructs the model to search the catalog and pick the best skill. |
| `use_skill(skill_name, task)` | Loads a chosen skill as the operating instructions. |
| `plan_skills_for_project(project)` | Assembles a set of skills across the STLC for a project. |

## Sharing with your QA team

`testskill-finder` speaks **Streamable HTTP**, so one person hosts it and everyone
else connects by URL. Bind to all interfaces and (optionally) require a shared token:

```powershell
# Trusted network, no auth
uv run skillfinder-mcp --transport http --host 0.0.0.0 --port 8010 --path /mcp

# LAN + shared bearer token (recommended)
$env:SKILLFINDER_AUTH_TOKEN = "a-long-random-team-secret"
uv run skillfinder-mcp --transport http --host 0.0.0.0 --port 8010 --path /mcp
```

Print this machine's share URL and a ready-to-paste client snippet:

```powershell
uv run skillfinder-mcp --host 0.0.0.0 --port 8010 --print-config
```

Or use the helper, which also opens the firewall port:

```powershell
$env:SKILLFINDER_AUTH_TOKEN = "a-long-random-team-secret"   # optional
./scripts/share_skillfinder.ps1 -Port 8010
```

### Teammate client config

Put this in `.mcp.json` (Claude Code, VS Code, Cursor, etc.):

```json
{
  "mcpServers": {
    "testskill-finder": {
      "type": "http",
      "url": "http://192.168.1.7:8010/mcp",
      "headers": { "Authorization": "Bearer a-long-random-team-secret" }
    }
  }
}
```

Omit `headers` when auth is off.

### Notes

- **Firewall** — allow inbound TCP on the port (the helper script does it, or run as Administrator:
  `New-NetFirewallRule -DisplayName "testskill-finder MCP" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8010`).
- **Reachability** — same network → the LAN IP works. Remote teammates → front it with
  `cloudflared tunnel --url http://127.0.0.1:8010` (or ngrok) and share the HTTPS URL, or host the server on a shared VM.
- **Keep it running** — the host machine must stay on; give it a static IP / reserved DHCP lease so the URL is stable.
- **Security** — without a token, anyone who can reach the port gets every tool. Use the token off-loopback, and add TLS (or a tunnel) before leaving your network.

## Adding a skill

Drop a folder containing a `SKILL.md` anywhere under `skills/`. The folder path
determines the category (first segment) and framework pack (second segment, if
present). Frontmatter fields used by the catalog:

```yaml
---
name: my-skill
description: >-
  Short "when to use this" summary.
license: MIT
metadata:
  author: You
  stlc-phase: Test Design
  version: 1.0.0
---

# My Skill
...instructions...
```

No server restart is required for a fresh process; an already-running server
re-scans when its catalog is refreshed. Authored skills live under categories the
upstream repo does not use (`08-`/`09-`/`10-`), so `sync_skills` never clobbers them.

## Configuration

| Env var | Purpose |
| --- | --- |
| `SKILLFINDER_SKILLS_DIR` | Override the skills folder (default: `<project>/skills`). |
| `SKILLFINDER_AUTH_TOKEN` | When set, require `Authorization: Bearer <token>` on HTTP requests. |

## License

The vendored skills retain their upstream **MIT** license
(`metadata.author: TheTestingAcademy`). Authored skills are MIT as well.
