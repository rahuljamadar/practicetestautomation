# TestCreator MCP

A local-first MCP server for searching and inspecting test cases in a CSV catalog. The catalog schema is discovered from the CSV header; no VWO-specific columns are assumed.

## Requirements

- Python 3.12, 3.13, or 3.14
- `uv`
- A UTF-8 CSV catalog (the source file is read-only)

The prompt history references `data/vwo_5000_test_cases.csv`, but that dataset is not currently in this project. Place the confirmed catalog at that path or set `TC_MCP_CSV_PATH` to its location.

## Install and test

```powershell
uv sync --extra dev
uv run pytest -q
```

## Connect over stdio

```powershell
uv run tc-mcp
```

For MCP clients that launch local processes, configure the command as `uv` with arguments `run`, `--directory`, `<absolute-path-to-this-project>`, `tc-mcp`.

## Connect over local HTTP

```powershell
uv run tc-mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp
```

Configure the MCP client or Inspector to use `http://127.0.0.1:8000/mcp`. HTTP runs in stateless mode. The default bind address is loopback; do not expose it publicly without an explicit deployment and security review.

## Current MCP interface

The initial schema-agnostic MVP exposes:

- Tools: `catalog_summary`, `catalog_schema`, `search_test_cases`, `filter_test_cases`, and `get_test_cases`
- Resources: `catalog://summary` and `catalog://schema`
- Prompts: `build_test_plan` and `find_reusable_tests`

Search is case-insensitive across all fields. Filters use exact, case-insensitive values. Results are capped at 100 rows per call. This is an initial interface, not the historical 21-tool inventory mentioned in `02_prompt.md`; the exact contracts should be finalized after the source CSV and prior plan are available.

The current server is read-only. No tool edits the source CSV or writes an overlay.
