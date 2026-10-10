# Test Cases Catalog

## Dataset Notice

`data/vwo_5000_test_cases.csv` is a **synthetic sample catalog generated for developing and demonstrating the TestCreator MCP**. It is not the historical VWO dataset mentioned in `02_prompt.md`, and its cases are not verified against VWO product behavior. Do not treat it as approved product coverage or use it as a substitute for the original source data.

## Contents

- 5,000 records with unique IDs from `TC-00001` through `TC-05000`
- 17 sample modules and 72 sample feature labels
- Scenario combinations covering successful actions, validation errors, permissions, network timeouts, concurrent changes, and repeated requests
- Priority, test type, browser, device, status, preconditions, steps, expected result, tags, and source fields
- Every row is marked `Synthetic sample for MCP development` in the `source` column

The records are generated deterministically from module/feature and action/condition combinations. This provides varied data for testing search, filters, bounded responses, and MCP Inspector without presenting generated cases as real production tests.

## CSV Schema

| Column | Meaning |
|---|---|
| `test_case_id` | Unique synthetic test-case identifier. |
| `module` | Sample product area. |
| `feature` | Sample feature within the module. |
| `scenario` | Unique action and condition combination. |
| `priority` | Sample priority from P1 through P4. |
| `test_type` | Functional, validation, access control, resilience, concurrency, or idempotency category. |
| `browser` | Sample browser label. |
| `device` | Sample device label. |
| `status` | Lifecycle status; all generated rows are `Active`. |
| `preconditions` | Setup assumptions for the scenario. |
| `steps` | Generic steps to exercise the scenario. |
| `expected_result` | Generic expected behavior for the condition. |
| `tags` | Semicolon-separated module, feature, and test-type labels. |
| `source` | Explicit synthetic-data marker. |

## Generate Again

From the `TestCase_Creator_MCP` directory:

```powershell
uv run python scripts/generate_sample_catalog.py
```

The generator writes the default catalog path used by the MCP. It uses only the Python standard library. A different output path or smaller sample can be selected with `--output` and `--count`.

## Try It in MCP Inspector

After generating the file, use the existing Inspector at `http://127.0.0.1:6274`. For example, search `campaign`, `variation`, or `network timeout`; `limit` defaults to 20 and cannot exceed 100.