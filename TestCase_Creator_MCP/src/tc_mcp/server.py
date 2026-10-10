from __future__ import annotations

import argparse
import os
from pathlib import Path

from fastmcp import FastMCP

from tc_mcp.catalog import Catalog, DEFAULT_LIMIT, MAX_LIMIT


DEFAULT_CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "vwo_5000_test_cases.csv"
CATALOG = Catalog(Path(os.environ.get("TC_MCP_CSV_PATH", DEFAULT_CSV_PATH)))
mcp = FastMCP("TestCreator MCP")


@mcp.tool(description="Report catalog availability, row count, and available fields.")
def catalog_summary() -> dict:
    return CATALOG.summary()


@mcp.tool(description="Return the catalog field names and an example of its structure.")
def catalog_schema() -> dict:
    summary = CATALOG.summary()
    if not summary["available"]:
        return summary
    sample = CATALOG.filter({}, limit=1)["results"]
    return {"fields": summary["fields"], "sample": sample}


@mcp.tool(description="Search all catalog fields for a case-insensitive text match.")
def search_test_cases(query: str, limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.search(query, limit)


@mcp.tool(description="Filter catalog rows by exact, case-insensitive field values.")
def filter_test_cases(filters: dict[str, str], limit: int = DEFAULT_LIMIT) -> dict:
    return CATALOG.filter(filters, limit)


@mcp.tool(description="Find rows whose selected field exactly matches a value.")
def get_test_cases(
    value: str, field: str | None = None, limit: int = DEFAULT_LIMIT
) -> dict:
    return CATALOG.get_test_cases(value, field, limit)


@mcp.resource("catalog://summary", description="Current catalog availability and counts.")
def catalog_summary_resource() -> dict:
    return CATALOG.summary()


@mcp.resource("catalog://schema", description="Catalog fields and one example row.")
def catalog_schema_resource() -> dict:
    summary = CATALOG.summary()
    if not summary["available"]:
        return summary
    return {"fields": summary["fields"], "sample": CATALOG.filter({}, limit=1)["results"]}


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the TestCreator MCP server")
    parser.add_argument("--transport", choices=("stdio", "http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--path", default="/mcp")
    arguments = parser.parse_args()

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
