# Architecture — testskill-finder MCP

## Overview

`testskill-finder` is a read-mostly MCP server over a folder of QA agent skills. It
follows the same architecture as the sibling `TestCase_Creator_MCP`: a pure data
layer wrapped by a FastMCP server that registers tools, resources and prompts with
decorators.

```
        ┌──────────────────────┐
        │   skills/ (50 SKILL.md)  │   ← single source of truth (filesystem)
        └────────────┬─────────┘
                     │ scan + parse frontmatter
                     ▼
        ┌──────────────────────┐        ┌──────────────────────┐
        │   catalog.SkillCatalog │◀──────│   sync.sync_skills     │
        │  search / rank / read  │       │  downloads upstream    │
        └────────────┬─────────┘        └──────────┬───────────┘
                     │                               │
                     ▼                               ▼
        ┌──────────────────────┐        ┌──────────────────────┐
        │   server.FastMCP       │        │  scripts/sync_skills  │
        │  "testskill-finder"    │        │      (CLI wrapper)    │
        └──────────────────────┘        └──────────────────────┘
```

## Components

### `catalog.py` — data layer (no MCP, no network)

- `SkillCatalog(skills_root)` walks the folder for `SKILL.md` files, parses the YAML
  frontmatter with PyYAML, and derives `category` (first path segment) and `pack`
  (second segment, e.g. `playwright-pack`).
- Malformed skills are skipped and reported rather than crashing the scan.
- Query methods: `summary`, `list_categories`, `list_skills`, `filter_skills`,
  `rank`, `recommend`, `get_skill`, `get_skill_metadata`, `list_skill_files`,
  `get_skill_file`, `search_in_skill`, `index`.
- `rank` scores each skill: exact-phrase and token hits in `name` > `description` >
  `body`, with a deterministic tie-break on skill name — the same shape as
  `TestCase_Creator_MCP.catalog.rank_test_cases`.
- `get_skill_file` guards against path traversal (rejects absolute paths and `..`,
  then verifies the resolved path stays inside the skill folder).
- Bounds reused from the reference: lists default to 20 and cap at 100.

### `sync.py` — upstream download

- Fetches one repository tarball (`codeload.github.com`) with the standard library
  (`urllib` + `tarfile`), extracts to a temp dir, and copies every folder containing
  a `SKILL.md` from `<repo>/skillmasterclass/skills/**` into `skills/<relative>`.
- `shutil.copytree(dirs_exist_ok=True)` preserves `references/`, `scripts/`,
  `copilot/` and assets, and overwrites only upstream-owned paths — never the
  authored `08-`/`09-`/`10-` categories.
- Returns an `added`/`updated`/`skipped`/`errors` report.

### `server.py` — MCP surface

- Single `mcp = FastMCP("testskill-finder")` instance with module-level
  `CATALOG = SkillCatalog(SKILLS_DIR)`.
- Tools/resources/prompts are thin delegations to the catalog, so the same logic is
  unit-tested directly in `tests/test_catalog.py`.
- A `sync_skills` tool tagged `write` is disabled by default via
  `mcp.disable(tags={"write"}, components={"tool"})` and re-enabled with
  `--enable-write-tools` (mirrors `TestCase_Creator_MCP`).
- A `@mcp.custom_route("/")` page explains that the endpoint is an MCP server.
- `main()` selects stdio (default) or stateless streamable HTTP.

## Data flow

1. Client calls `search_skills("playwright api")`.
2. `SkillCatalog.rank` tokenizes, scores every skill, and returns the top matches
   (e.g. `pw-api-tester`, `api-test-designer`).
3. Client calls `get_skill("pw-api-tester")` to load the full instructions, or reads
   the `skills://skill/pw-api-tester` resource.

## Testing strategy

- `tests/test_catalog.py` builds a temporary skills tree (valid + malformed) and
  asserts scanning, frontmatter parsing, ranking determinism, file reads and
  path-traversal rejection.
- `tests/test_server.py` drives the live server in-process with FastMCP's `Client`,
  asserting the tool/resource/prompt surface, the write-tool gating, and that the
  shipped catalog contains at least 50 skills.
