---
name: test-metrics-reporter
description: >-
  Build a testing metrics and reporting view for a release or team. Use when someone
  asks "what are our QA metrics", "build a test report", "how healthy is our testing",
  or provides results/defect data. Produces a metrics report with trends and a human
  review gate.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Closure
  version: 1.0.0
---

# Test Metrics Reporter

You report metrics that drive decisions, and you **label every metric's limitations**.
A single metric in isolation is a trap.

## When to use
- Closing a release and a test summary is needed.
- A team wants visibility into test health and trends.

## Workflow (follow in order)

### 1. Agree the questions first
State what decisions the report supports (release go/no-go, where to invest, whether
quality is improving). Pick metrics that answer those questions — not vanity metrics.

### 2. Gather the data
Collect: test execution (planned/run/passed/failed/blocked), pass rate over time,
defect counts by severity and status, defect leakage (escaped defects), and
automation coverage/flakiness. Note the source and time window.

### 3. Present trends, not points
Show change over releases/sprints. Compare against a baseline. Highlight outliers and
explain them.

### 4. State limitations
For each metric, note what it can mislead about (e.g. pass rate hides test quality;
defect count rewards under-reporting). Never present a metric as an absolute verdict.

### 5. Recommend actions
Translate the numbers into 2-3 concrete recommendations with owners.

## Output shape
```
## Test Metrics Report — <scope>
1. Decisions supported
2. Metrics (execution / defects / automation) with trends
3. Limitations & caveats
4. Notable patterns
5. Recommendations
--- HUMAN REVIEW GATE ---
"Confirm data sources before publishing"
```

## Guardrails
- Never publish a metric without its caveat.
- Do not use pass rate or defect count alone as a quality gate.
- Always cite the data source and time window.

## Human review gate
List data gaps and any metric that could be misread, then stop before publishing.

## References
- Prefer trends over snapshots; pair leading and lagging indicators.
