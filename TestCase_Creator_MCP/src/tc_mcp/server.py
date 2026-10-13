from __future__ import annotations

import argparse
import os
from pathlib import Path

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse

from tc_mcp.bootstrap import ensure_sample_catalog
from tc_mcp.catalog import Catalog, DEFAULT_LIMIT, MAX_LIMIT
from tc_mcp.overlay import CatalogOverlay


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "vwo_5000_test_cases.csv"
CSV_PATH = (
    Path(os.environ["TC_MCP_CSV_PATH"]).expanduser()
    if os.environ.get("TC_MCP_CSV_PATH")
    else DEFAULT_CSV_PATH
)
if not os.environ.get("TC_MCP_CSV_PATH"):
    ensure_sample_catalog(
        DEFAULT_CSV_PATH, PROJECT_ROOT / "scripts" / "generate_sample_catalog.py"
    )
OVERLAY_PATH = Path(
    os.environ.get("TC_MCP_OVERLAY_PATH", PROJECT_ROOT / "data" / "test_case_overlay.json")
).expanduser()
CATALOG = Catalog(CSV_PATH)
OVERLAY = CatalogOverlay(OVERLAY_PATH)
mcp = FastMCP("TestCreator MCP")


@mcp.custom_route("/", methods=["GET"], include_in_schema=False)
async def browser_help(request: Request) -> HTMLResponse:
    del request
    return HTMLResponse(
        """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TestCreator MCP</title><body style="font:16px system-ui;max-width:720px;margin:12vh auto;padding:24px;color:#18212b">
<h1>TestCreator MCP</h1><p>This is an MCP endpoint, not a regular website.</p>
<p>Connect an MCP client or open MCP Inspector and use the Streamable HTTP URL:</p>
<p><code>http://127.0.0.1:8000/mcp</code></p>
<p>Inspector: <a href="http://127.0.0.1:6274">http://127.0.0.1:6274</a></p>
</body></html>"""
    )


@mcp.tool(description="Report catalog availability, row count, and available fields.")
def catalog_summary() -> dict:
    return CATALOG.summary()


@mcp.tool(description="Return catalog field names and one example record.")
def catalog_schema() -> dict:
    summary = CATALOG.summary()
    if not summary["available"]:
        return summary
    return {"fields": summary["fields"], "sample": CATALOG.browse(limit=1)["results"]}


@mcp.tool(description="Return row, field, unique-value, and missing-value counts.")
def catalog_statistics() -> dict:
    return CATALOG.statistics()


@mcp.tool(description="List distinct values and their counts for a catalog field.")
def list_catalog_values(
    field: str, filters: dict[str, str] | None = None, limit: int = MAX_LIMIT
) -> dict:
    return CATALOG.list_values(field, limit, filters)


@mcp.tool(description="Search all catalog fields for a case-insensitive text match.")
def search_test_cases(query: str, limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.search(query, limit)


@mcp.tool(description="Find rows whose selected field exactly matches a value.")
def get_test_cases(
    value: str, field: str | None = None, limit: int = DEFAULT_LIMIT
) -> dict:
    return CATALOG.get_test_cases(value, field, limit)


@mcp.tool(description="Retrieve one test case by its test_case_id.")
def get_test_case(test_case_id: str) -> dict:
    return CATALOG.get_test_cases_by_ids([test_case_id], limit=1)


@mcp.tool(description="Retrieve several test cases by ID and report IDs not found.")
def get_test_cases_by_ids(test_case_ids: list[str], limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.get_test_cases_by_ids(test_case_ids, limit)


@mcp.tool(description="Filter catalog rows by exact, case-insensitive field values.")
def filter_test_cases(filters: dict[str, str], limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.filter(filters, limit)


@mcp.tool(description="Browse a bounded page of catalog records.")
def browse_test_cases(offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.browse(offset, limit)


@mcp.tool(description="List modules and the number of cases in each module.")
def list_modules(limit: int = MAX_LIMIT) -> dict:
    return CATALOG.list_values("module", limit)


@mcp.tool(description="List features, optionally restricted to a module.")
def list_features(module: str | None = None, limit: int = MAX_LIMIT) -> dict:
    filters = {"module": module} if module else None
    return CATALOG.list_values("feature", limit, filters)


@mcp.tool(description="Summarize test-case coverage grouped by a catalog field.")
def get_coverage_report(
    group_by: str = "module",
    filters: dict[str, str] | None = None,
    limit: int = DEFAULT_LIMIT,
) -> dict:
    return CATALOG.coverage_report(group_by, filters, limit)


@mcp.tool(description="Report missing values, duplicate identifiers/scenarios, and lifecycle states.")
def get_data_quality_report() -> dict:
    return CATALOG.data_quality_report()


@mcp.tool(description="Find duplicate values across one or more catalog fields.")
def find_duplicate_test_cases(
    fields: list[str] | None = None, limit: int = DEFAULT_LIMIT
) -> dict:
    return CATALOG.duplicate_groups(fields, limit)


@mcp.tool(description="Find cases marked deprecated, retired, obsolete, or inactive.")
def find_deprecated_test_cases(limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.deprecated_cases(limit)


@mcp.tool(description="Rank matching test cases with a deterministic relevance and priority score.")
def rank_test_cases(
    query: str,
    module: str | None = None,
    feature: str | None = None,
    priority: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> dict:
    return CATALOG.rank_test_cases(query, module, feature, priority, limit)


@mcp.tool(description="Recommend relevant existing test cases for a feature or behavior.")
def recommend_test_cases(
    feature_or_behavior: str, module: str | None = None, limit: int = DEFAULT_LIMIT
) -> dict:
    return CATALOG.rank_test_cases(feature_or_behavior, module=module, limit=limit)


@mcp.tool(description="Build a bounded test-plan draft from matching catalog cases.")
def create_test_plan(feature: str, risk: str = "", limit: int = DEFAULT_LIMIT) -> dict:
    matches = CATALOG.rank_test_cases(feature, limit=limit)
    return {
        "feature": feature,
        "risk_context": risk or "Not provided",
        "matched_cases": matches["results"],
        "total_matches": matches["total_matches"],
        "coverage_note": "Review the returned cases against the stated risk; this draft does not assert unverified coverage.",
    }


@mcp.tool(tags={"write"}, description="Save a note and optional tags in the separate overlay, never in the CSV.")
def annotate_test_case(test_case_id: str, note: str, tags: list[str] | None = None) -> dict:
    existing = CATALOG.get_test_cases_by_ids([test_case_id], limit=1)
    if not existing["results"]:
        raise ValueError(f"Unknown test_case_id: {test_case_id}")
    return OVERLAY.annotate(test_case_id, note, tags)


@mcp.tool(tags={"write"}, description="Save a bounded filtered selection in the separate overlay JSON.")
def export_test_cases(
    name: str, filters: dict[str, str], limit: int = MAX_LIMIT
) -> dict:
    selected = CATALOG.filter(filters, limit)
    return OVERLAY.export(name, selected["results"])


mcp.disable(tags={"write"}, components={"tool"})


@mcp.resource("catalog://summary", description="Current catalog availability and counts.")
def catalog_summary_resource() -> dict:
    return CATALOG.summary()


@mcp.resource("catalog://schema", description="Catalog fields and one example row.")
def catalog_schema_resource() -> dict:
    return catalog_schema()


@mcp.resource("catalog://coverage", description="Module coverage for the current catalog.")
def catalog_coverage_resource() -> dict:
    return CATALOG.coverage_report("module")


@mcp.resource("catalog://data-quality", description="Missing values and catalog quality indicators.")
def catalog_data_quality_resource() -> dict:
    return CATALOG.data_quality_report()


@mcp.prompt(description="Create a focused test plan using relevant catalog cases.")
def build_test_plan(feature: str, risk: str = "") -> str:
    return (
        "Use the TestCreator MCP catalog to identify existing cases for this feature. "
        "Prefer relevant, non-duplicate cases and explain any coverage gaps. "
        f"Feature: {feature}\nRisk context: {risk or 'Not provided'}"
    )


@mcp.prompt(description="Find reusable catalog test cases for a feature or behavior.")
def find_reusable_tests(feature_or_behavior: str) -> str:
    return (
        "Search the catalog for test cases relevant to the following feature or behavior. "
        "Summarize why each returned case is relevant and do not invent catalog fields.\n"
        f"Request: {feature_or_behavior}"
    )


@mcp.prompt(description="Review catalog coverage and identify gaps for a feature or module.")
def review_coverage_gaps(feature_or_module: str) -> str:
    return (
        "Inspect TestCreator MCP coverage for the requested feature or module. "
        "Use available catalog fields only, cite matching case IDs, and distinguish missing "
        "catalog evidence from missing product coverage.\n"
        f"Request: {feature_or_module}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the TestCreator MCP server")
    parser.add_argument("--transport", choices=("stdio", "http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--path", default="/mcp")
    parser.add_argument(
        "--enable-write-tools", action="store_true",
        help="Expose annotation and export tools that write only to the overlay JSON.",
    )
    arguments = parser.parse_args()

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
