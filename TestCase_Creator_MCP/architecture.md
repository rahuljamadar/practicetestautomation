# TestCreator MCP Architecture

## Status

The project implements a reconstructed 21-tool TestCreator MCP: 19 read-only tools are visible by default, and two overlay-writing tools can be explicitly enabled. The historical detailed tool plan is not in this checkout, so the names and contracts are grounded in `02_prompt.md`, `objective.md`, and the available CSV schema rather than claimed to be an exact recovery.

## What We Are Building

A standalone Python MCP server that lets QA engineers and developers discover and inspect test cases in a CSV catalog through standard MCP clients. FastMCP exposes the catalog operations as tools, resources, and prompts. The server reads the original CSV and does not modify it.

The implementation is separate from the workspace's Playwright/Node project. It supports local stdio for process-based MCP clients and local stateless HTTP for clients such as MCP Inspector.

## Current Components

| Component | Location | Responsibility |
|---|---|---|
| MCP registration and startup | `src/tc_mcp/server.py` | Registers MCP tools, resources, and prompts; starts stdio or stateless HTTP transport. |
| CSV catalog access | `src/tc_mcp/catalog.py` | Reads UTF-8 CSV data, discovers fields from the header, searches, filters, profiles, ranks, and bounds results. |
| Missing default data | `src/tc_mcp/bootstrap.py`, `scripts/generate_sample_catalog.py` | Creates the synthetic 5,000-row development CSV only when the default file is missing. |
| Separate edits/exports | `src/tc_mcp/overlay.py` | Stores annotations and named exports in JSON without modifying the source CSV. |
| Project/dependencies | `pyproject.toml`, `uv.lock` | Declares Python compatibility, FastMCP 4.1.0, the `tc-mcp` command, and development dependencies. |
| Behavior tests | `tests/test_catalog.py` | Exercises schema discovery, search, filtering, lookup, missing-file reporting, field validation, and result limits with fixture CSV data. |
| User setup | `README.md` | Describes installation, data path configuration, and local client connection methods. |

## Data Flow

1. The server resolves the catalog path from `TC_MCP_CSV_PATH`, or uses the default `data/vwo_5000_test_cases.csv` beneath the project root. If the default file is absent, the synthetic sample generator creates it; a missing custom path is not generated automatically.
2. A tool or resource calls the shared `Catalog` interface.
3. `Catalog` reads the CSV as UTF-8 with optional BOM support and discovers columns from the header; no VWO-specific column names are assumed.
4. The requested operation returns structured records or summary information. List results default to 20 and cannot exceed 100.
5. FastMCP returns the result to the connected MCP client. The server does not write to the source CSV or create an overlay.

If the file is missing or has no header, summary/schema operations report that the catalog is unavailable. Search and record operations require a readable CSV and report errors for invalid fields, empty search text, or invalid limits.

## MCP Tools

| Group | Tools |
|---|---|
| Catalog overview | `catalog_summary`, `catalog_schema`, `catalog_statistics`, `list_catalog_values` |
| Search and lookup | `search_test_cases`, `get_test_cases`, `get_test_case`, `get_test_cases_by_ids` |
| Filtering and browsing | `filter_test_cases`, `browse_test_cases`, `list_modules`, `list_features` |
| Coverage and data quality | `get_coverage_report`, `get_data_quality_report`, `find_duplicate_test_cases`, `find_deprecated_test_cases` |
| Selection and planning | `rank_test_cases`, `recommend_test_cases`, `create_test_plan` |
| Curation and export | `annotate_test_case`, `export_test_cases` |

The two curation/export tools carry the `write` tag and are hidden by default. Pass `--enable-write-tools` to expose them. They write only to the JSON overlay, never to the CSV.

## Current Resources and Prompts

Resources: `catalog://summary`, `catalog://schema`, `catalog://coverage`, and `catalog://data-quality`.

Prompts: `build_test_plan`, `find_reusable_tests`, and `review_coverage_gaps`. Prompts guide the connected model; tools perform catalog operations.

## Planned Tool Groups

The prompt history reports a target of 21 tools in six groups, but does not preserve the tool names or detailed contracts. The following groups are a proposed way to organize that future interface, not a claim that those tools already exist:

1. **Catalog overview**: summarize dataset size, fields, and available categories.
2. **Search and lookup**: find cases by text, identifier, or confirmed catalog fields.
3. **Filtering and browsing**: narrow cases by module, feature, priority, type, browser, device, or other fields only when present in the verified CSV.
4. **Coverage and data quality**: report category coverage and identify duplicates, deprecated cases, missing values, or malformed labels when confirmed by profiling.
5. **Test selection and planning**: rank or recommend relevant cases using a documented, deterministic scoring method and provide coverage-oriented planning support.
6. **Curation and export**: only if approved, propose edits or export selections through a separate overlay/output path; keep write-capable operations disabled by default.

Before expanding the current tool surface, profile the real CSV, recover or approve the detailed tool inventory, set response limits, and test each tool contract.

## Safety and Deployment Boundaries

- Default to local-only operation. Do not start a public tunnel or expose the service without explicit authorization.
- Bind HTTP to `127.0.0.1` by default and use stateless HTTP.
- Treat the source catalog as immutable. Curation writes to a separate overlay, never the source CSV.
- Keep write-capable tools unavailable by default.
- Validate requested fields and limits; cap response sizes to protect MCP clients.
- Avoid logging or returning unrelated local file contents.

## Run and Connect

Stdio:

```powershell
uv run tc-mcp
```

Local stateless HTTP:

```powershell
uv run tc-mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp
```

The local HTTP MCP endpoint is `http://127.0.0.1:8000/mcp`.

## Verification Strategy

- Run `uv run pytest -q` for catalog behavior and edge cases.
- Use a real MCP client to verify tool/resource/prompt discovery and representative calls over stdio and local HTTP.
- Verify field discovery, record counts, data-quality handling, search/filter behavior, ranking, generation-on-missing, and response limits against fixture and sample data.
- Test that overlay writes are hidden by default, edits are isolated to the overlay, and the source CSV remains unchanged.
