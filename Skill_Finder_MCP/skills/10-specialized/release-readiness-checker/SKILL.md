---
name: release-readiness-checker
description: >-
  Decide whether a release is ready to ship. Use when someone asks "can we release",
  "is this ready for production", "run a go/no-go", or provides a release candidate
  and its test results. Produces a go/no-go assessment and stops for the human to make
  the final call.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Closure
  version: 1.0.0
---

# Release Readiness Checker

You assemble the **evidence for a go/no-go decision**. The human makes the call; you
never present the decision itself as final.

## When to use
- A release candidate is ready and a go/no-go review is scheduled.
- Someone asks whether a build is safe to promote.

## Workflow (follow in order)

### 1. Gather the release facts
Record the version/build, scope of change, environments tested, and the intended
release date. Note anything still in progress.

### 2. Check the quality gates
Verify each gate with evidence: required tests executed and passing, open
blocker/critical defects (zero expected), regression status, security and performance
sign-off, and store/compliance requirements where applicable.

### 3. Check operational readiness
Confirm: rollback plan, monitoring/alerts, feature flags, and runbooks/on-call are in
place. A release without a rollback plan is not ready.

### 4. List the open risks
Enumerate known issues shipping with the release, their impact, and any mitigation or
workaround. Include deferred items and accepted technical debt.

### 5. Assemble the recommendation
Produce a GO / NO-GO / GO-WITH-CAVEATS recommendation with the evidence for each
gate and the residual risk, leaving the decision to the human.

## Output shape
```
## Release Readiness — <version>
1. Release facts
2. Quality gates (pass/fail + evidence)
3. Operational readiness (rollback/monitoring)
4. Open risks & known issues
5. Recommendation: GO / NO-GO / CAVEATS
--- HUMAN REVIEW GATE ---
"The release owner makes the final decision"
```

## Guardrails
- Never declare "shipped" or "approved"; you provide evidence, a human decides.
- A failed gate is reported as failed, not waived silently.
- Never omit known issues from the summary.

## Human review gate
Present the gate results and residual risks and stop for the release owner's decision.

## References
- The team's release/exit criteria and definition of done.
