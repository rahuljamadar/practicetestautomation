# TestCreator MCP

A local-first FastMCP server for discovering, reviewing, ranking, and exporting test cases from a CSV catalog. The source CSV is never modified. The server exposes 21 tools, four resources, and three prompts; its two overlay-writing tools are hidden unless explicitly enabled.

## Data

`data/vwo_5000_test_cases.csv` is a **synthetic development sample**, not a verified VWO export. If the default file is missing, the server creates 5,000 synthetic rows on startup. If `TC_MCP_CSV_PATH` is set, that custom path is used as-is and is not populated automatically. Set it only to a catalog you have verified.

## Requirements and Tests

- Python 3.12, 3.13, or 3.14
- `uv`

```powershell
uv sync --extra dev
uv run pytest -q
```

## Connect

On Windows, start both local services with one command:

```powershell
.\scripts\start_testcreator_mcp.ps1
```

The launcher starts the MCP server if port 8000 is free and runs Inspector in the same terminal if port 6274 is free. Inspector opens a browser with a fresh authenticated URL and prints that URL in the terminal; keep the terminal open while using Inspector. Its tokenized URL changes after an Inspector restart. If Inspector is already running, the current tokenized URL remains valid.

Stdio for process-based MCP clients:

```powershell
uv run tc-mcp
```

Local stateless HTTP:

```powershell
uv run tc-mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp
```

Use `http://127.0.0.1:8000/mcp` as the Streamable HTTP MCP endpoint. Opening `http://127.0.0.1:8000/` in a browser shows connection help. To open MCP Inspector preconfigured for this server:

```powershell
npx @modelcontextprotocol/inspector --transport http --server-url http://127.0.0.1:8000/mcp
```

The server binds to loopback by default. Do not expose it publicly without an explicit deployment and security review.

## MCP Interface

Catalog overview: `catalog_summary`, `catalog_schema`, `catalog_statistics`, `list_catalog_values`.

Search and lookup: `search_test_cases`, `get_test_cases`, `get_test_case`, `get_test_cases_by_ids`.

Filtering and browsing: `filter_test_cases`, `browse_test_cases`, `list_modules`, `list_features`.

Coverage and quality: `get_coverage_report`, `get_data_quality_report`, `find_duplicate_test_cases`, `find_deprecated_test_cases`.

Selection and planning: `rank_test_cases`, `recommend_test_cases`, `create_test_plan`.

Curation and export: `annotate_test_case`, `export_test_cases`. These two tools write only to `data/test_case_overlay.json` (or `TC_MCP_OVERLAY_PATH`) and are disabled by default. Enable them explicitly with `uv run tc-mcp --enable-write-tools` (add the desired transport options as needed).

Resources: `catalog://summary`, `catalog://schema`, `catalog://coverage`, and `catalog://data-quality`.

Prompts: `build_test_plan`, `find_reusable_tests`, and `review_coverage_gaps`.

Search is case-insensitive; filters use exact case-insensitive values. List responses default to 20 and are capped at 100. The ranking score is deterministic and favors textual relevance, higher priority, and active cases. The historical plan with exact tool contracts is not in this checkout, so this inventory is a documented reconstruction from `02_prompt.md`, `objective.md`, and the confirmed CSV schema.
