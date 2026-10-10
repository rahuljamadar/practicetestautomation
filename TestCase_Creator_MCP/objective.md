# TestCreator MCP Objective

## Purpose

Build a standalone, local-first Model Context Protocol (MCP) server that helps QA engineers and developers discover, inspect, select, and reuse test cases from a VWO test-case catalog. The server will expose the catalog through MCP tools, resources, and prompts so compatible AI clients can assist with test planning using consistent, bounded results.

## Problem

Test cases stored in a CSV catalog are difficult to explore consistently by hand. QA and development teams need a practical way to search and filter the catalog, understand its coverage, and identify relevant existing scenarios without editing the source data or manually processing large result sets.

## Intended Users

- QA engineers planning and maintaining test coverage
- Developers looking for relevant existing scenarios while changing a feature
- MCP client users who need catalog information through a standard interface

## Product Goals

- Load and inspect the VWO test-case catalog after its actual schema and location are confirmed.
- Support useful catalog discovery operations such as search, filtering, summaries, and relevant-test selection, based on fields that exist in the supplied data.
- Return clear, deterministic, size-limited results suitable for MCP clients.
- Make the server straightforward to run locally and connect through stdio or HTTP.
- Allow controlled catalog annotations or edits only if they are part of the approved tool contract; keep those changes separate from the original CSV.

## Data and Assumptions

The prompt history describes a 5,000-row VWO test-case CSV at `data/vwo_5000_test_cases.csv` and reports duplicate scenarios, deprecated cases, and inconsistent labels. Those details are historical claims, not verified properties of the data currently available in this workspace. Before implementing data-specific behavior, obtain the CSV, confirm its path and schema, and profile its rows and quality issues.

The prompt history also reports a design of 21 tools across six groups, four resources, and three prompts. Their names and contracts are not present in the available files, so they must be recovered or designed and reviewed before implementation.

## Constraints and Safety

- Implement the MCP as an independent Python project using FastMCP; do not couple it to the workspace's root Playwright/Node project.
- Treat the source CSV as read-only. Never rewrite or overwrite it.
- Keep the server local by default. Support stdio and local stateless HTTP; do not create a public tunnel or expose the service publicly unless explicitly requested.
- Keep write-capable tools disabled by default. If approved, persist changes in a separate overlay and make the behavior explicit to the client.
- Bound response sizes and validate inputs so large catalogs do not produce unmanageable MCP responses.
- Do not claim catalog counts, field names, tool counts, or data-quality behavior as verified until checked against the actual source files.

## Out of Scope

- Public hosting or temporary internet exposure by default
- Modifying the source CSV in place
- Changing the root Playwright/Node project or its dependencies
- Implementing data-specific filters or classifications based only on unverified prompt-history claims

## Success Criteria

- The project can be started locally and connected to by a compatible MCP client over stdio and stateless HTTP.
- MCP clients can discover and use the approved tools, resources, and prompts to retrieve bounded catalog information.
- Catalog behavior is covered by tests using the confirmed schema, including relevant malformed, duplicate, deprecated, or inconsistent data cases found during profiling.
- Write operations, if approved, are unavailable by default and cannot alter the source CSV; overlay behavior is tested separately.
- Setup, configuration, connection options, data placement, and write-safety behavior are documented.
