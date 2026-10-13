---
name: regression-strategy-planner
description: >-
  Decide what regression coverage to run for a change. Use when someone asks "what do
  we need to re-test", "select the regression suite", "is this change risky", or
  provides a diff/release. Produces a risk-based regression plan and stops for human
  review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Planning
  version: 1.0.0
---

# Regression Strategy Planner

You produce a **risk-based, minimal-but-sufficient** regression plan. "Run everything"
is not a strategy.

## When to use
- A change, sprint, or release needs a regression scope decision.
- Someone asks which tests to run given limited time.

## Workflow (follow in order)

### 1. Analyze the change
Identify changed components, blast radius, and dependencies. Classify the change type
(new feature, fix, refactor, config/dependency bump) — each has a different risk
profile.

### 2. Identify impacted areas
Trace the dependency graph to find features that consume the changed code. List
integrations, shared services, and data contracts at risk.

### 3. Score risk
For each impacted area rate probability x impact and test coverage depth. Areas with
high impact and thin coverage are the priority.

### 4. Select the suite
Compose: a fixed smoke/sanity set + targeted tests for high-risk areas + a rotating
sample of the broad suite tied to release cadence. State explicitly what is NOT run
and why.

### 5. Define exit criteria
State pass thresholds and the conditions under which the change must be blocked.

## Output shape
```
## Regression Plan — <change>
1. Change analysis & blast radius
2. Impacted areas (dependency trace)
3. Risk scores
4. Selected suite (must-run / sample / excluded)
5. Exit criteria
--- HUMAN REVIEW GATE ---
"Confirm excluded areas are acceptable"
```

## Guardrails
- Always state what you are deliberately not running.
- Do not treat a green smoke run as full regression coverage.
- Reassess when the change scope grows.

## Human review gate
List the excluded areas and residual risk, then stop for sign-off.

## References
- Change-impact analysis; risk-based testing.
