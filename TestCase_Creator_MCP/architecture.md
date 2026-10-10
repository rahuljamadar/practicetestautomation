# TestCreator MCP Architecture

## Status

This document describes the current schema-agnostic MVP and the proposed direction for the full TestCreator MCP. The VWO CSV and the historical detailed tool plan referenced by `02_prompt.md` are not present in this project. Therefore, data-specific tool names and contracts remain subject to review after those inputs are available.

## What We Are Building

A standalone Python MCP server that lets QA engineers and developers discover and inspect test cases in a CSV catalog through standard MCP clients. FastMCP exposes the catalog operations as tools, resources, and prompts. The server reads the original CSV and does not modify it.

The implementation is separate from the workspace's Playwright/Node project. It supports local stdio for process-based MCP clients and local stateless HTTP for clients such as MCP Inspector.

## Current Components

| Component | Location | Responsibility |
|---|---|---|
| MCP registration and startup | `src/tc_mcp/server.py` | Registers MCP tools, resources, and prompts; starts stdio or stateless HTTP transport. |
| CSV catalog access | `src/tc_mcp/catalog.py` | Reads UTF-8 CSV data, discovers fields from the header, searches and filters records, and bounds result counts. |
| Project/dependencies | `pyproject.toml`, `uv.lock` | Declares Python compatibility, FastMCP 4.1.0, the `tc-mcp` command, and development dependencies. |
| Behavior tests | `tests/test_catalog.py` | Exercises schema discovery, search, filtering, lookup, missing-file reporting, field validation, and result limits with fixture CSV data. |
| User setup | `README.md` | Describes installation, data path configuration, and local client connection methods. |

## Data Flow

1. The server resolves the catalog path from `TC_MCP_CSV_PATH`, or uses the default `data/vwo_5000_test_cases.csv` beneath the project root.
2. A tool or resource calls the shared `Catalog` interface.
3. `Catalog` reads the CSV as UTF-8 with optional BOM support and discovers columns from the header; no VWO-specific column names are assumed.
4. The requested read operation returns structured records or summary information. List results default to 20 and cannot exceed 100.
5. FastMCP returns the result to the connected MCP client. The server does not write to the source CSV or create an overlay.

If the file is missing or has no header, summary/schema operations report that the catalog is unavailable. Search and record operations require a readable CSV and report errors for invalid fields, empty search text, or invalid limits.

## Current MCP Tools

| Tool | Purpose |
|---|---|
| `catalog_summary` | Report whether the CSV is available, its row count, and discovered fields. |
| `catalog_schema` | Return discovered field names and one sample row. |
| `search_test_cases` | Search all fields for a case-insensitive substring; returns a bounded result set and total match count. |
| `filter_test_cases` | Filter by one or more exact, case-insensitive field values. |
| `get_test_cases` | Return rows where a selected field exactly matches a value; defaults to the first CSV column. |

All five current tools are read-only.

## Current Resources and Prompts

Resources:

- `catalog://summary` provides the current catalog availability and summary.
- `catalog://schema` provides the discovered fields and a sample row.

Prompts:

- `build_test_plan` frames a request to use relevant catalog cases for feature/risk-based test planning.
- `find_reusable_tests` frames a request to locate reusable cases for a feature or behavior.

Prompts guide the connected model; they do not independently perform catalog search.

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
- Treat the source catalog as immutable. Any future curation must write to a separate overlay, never the source CSV.
- Keep future write-capable tools unavailable by default.
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
- When the actual CSV is added, verify field discovery, record counts, data-quality handling, search/filter behavior, and response limits against it.
- If overlay writes are later approved, test that writes are hidden by default, edits are isolated to the overlay, and the source CSV remains byte-for-byte unchanged.
