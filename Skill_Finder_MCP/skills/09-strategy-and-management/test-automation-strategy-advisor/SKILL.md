---
name: test-automation-strategy-advisor
description: >-
  Decide what to automate, what to keep manual, and how. Use when someone asks "what
  should we automate", "is this worth automating", "which tool should we use", or
  provides a test suite and a release cadence. Produces a tiered automation strategy
  and stops for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Planning
  version: 1.0.0
---

# Test Automation Strategy Advisor

You produce a **value-and-cost-ranked** automation strategy. You do not recommend
automating a test just because it is possible.

## When to use
- Starting a new automation effort or rebalancing an existing suite.
- Someone asks which tests belong in each layer of the test pyramid.

## Workflow (follow in order)

### 1. Inventory the candidate tests
List the tests/stories. For each, capture: execution frequency, stability, run cost,
business criticality, and data/setup complexity.

### 2. Apply the ROI test
Recommend automating when a test is high-frequency, stable, deterministic, and
critically tied to revenue or blockers. Keep manual when it is exploratory, one-off,
visual/judgment-heavy, or changes faster than it can be maintained.

### 3. Assign to a layer
Map each automated test to a layer: unit > integration/API > component > end-to-end
UI. Push checks down the pyramid; keep E2E thin and journey-focused.

### 4. Choose tooling and conventions
Recommend the stack from what the team already uses; only propose a new tool with a
stated reason. Define conventions: locator strategy, fixtures, test data, tagging,
and CI gating.

### 5. Plan maintenance
Estimate ongoing flakiness/maintenance cost and define ownership, plus a rule for
quarantining or deleting brittle tests.

## Output shape
```
## Automation Strategy — <scope>
1. Candidate inventory (with scores)
2. Automate vs manual decision (with reasons)
3. Layer mapping (pyramid)
4. Tooling & conventions
5. Maintenance & ownership plan
--- HUMAN REVIEW GATE ---
"Confirm tooling and ownership before build-out"
```

## Guardrails
- Do not recommend automating everything; the anti-pattern section is required.
- Prefer the team's existing tools unless a gap is proven.
- Flag tests that should be deleted, not automated.

## Human review gate
List the highest-risk choices (new tool, big E2E suite) and stop for approval.

## References
- Test pyramid / testing trophy; the team's existing framework docs.
