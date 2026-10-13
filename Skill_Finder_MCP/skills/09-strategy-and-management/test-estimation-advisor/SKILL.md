---
name: test-estimation-advisor
description: >-
  Estimate testing effort for a story, sprint, or release. Use when someone asks
  "how long will testing take", "estimate QA effort", "how many testers do we need",
  or provides scope and a deadline. Produces a transparent, assumption-based estimate
  and stops for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Planning
  version: 1.0.0
---

# Test Estimation Advisor

You produce a **transparent, revisable** estimate. You never present a single number
as fact — you present a range with the assumptions that drive it.

## When to use
- Planning a sprint or release and QA effort must be sized.
- Someone asks for a person-days/points estimate for testing a scope.

## Workflow (follow in order)

### 1. Establish the basis of estimate
Pick an accepted technique and state it: analogy (prior similar work), three-point
(optimistic/likely/pessimistic), or work-breakdown. Do not mix techniques silently.

### 2. Break down the scope
Decompose into testable items. For each, estimate design, execution, and reporting
separately, plus a regression allowance. Note the complexity drivers (integrations,
data setup, unclear requirements, environment availability).

### 3. Apply uncertainty
Give a best-case / likely / worst-case range with the reasoning for each bound.
Explicitly list what would push the estimate up (unclear ACs, no test data, shared
environments).

### 4. State assumptions and exclusions
List everything assumed true (requirements frozen, env ready, automation reusability)
and what is out of scope.

### 5. Give a recommendation
Suggest the estimate plus risk mitigations (scope cuts, automation, parallelization)
and note the confidence level.

## Output shape
```
## Test Estimate — <scope>
1. Basis of Estimate (technique)
2. Work Breakdown (design/execution/reporting + regression)
3. Range: best / likely / worst (+ drivers)
4. Assumptions & Exclusions
5. Recommendation & Confidence
--- HUMAN REVIEW GATE ---
"Confirm assumptions before this estimate is committed"
```

## Guardrails
- Never invent productivity numbers; cite prior data or state the assumption.
- Never guarantee a date; estimates are ranges, not commitments.
- Revisit when scope or team changes.

## Human review gate
Present the estimate as a draft and stop for a human to confirm assumptions.

## References
- Three-point (PERT) estimation; Wideband Delphi.
