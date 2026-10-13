---
name: test-environment-manager
description: >-
  Plan and validate test environments and test data. Use when someone asks "do we have
  the right environments", "what data do we need", "why is the env broken", or
  provides a release's environment needs. Produces an environment and data readiness
  plan and stops for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Planning
  version: 1.0.0
---

# Test Environment Manager

You ensure **environments and data are ready before execution** and that failures are
not misattributed to the product.

## When to use
- Before a test cycle, when environments or data must be provisioned.
- When "it works on my machine" or environment flakiness is suspected.

## Workflow (follow in order)

### 1. Map required environments
List each environment (dev/QA/staging/perf), its purpose, version of the app, and
third-party dependencies (payment sandbox, identity provider, email). Note
who owns it.

### 2. Define the configuration matrix
For each environment capture OS/browser/device targets, backend versions, feature
flags, and network conditions. Flag drift risk between environments.

### 3. Plan test data
Specify data sets per scenario, how they are created (seed, API, masked copy), how
they are reset between runs, and how PII is handled. Define a reuse vs fresh-data
policy.

### 4. Define a readiness checklist
Produce a go/no-go checklist: services up, smoke passes, data seeded, credentials
valid, observability (logs/metrics) reachable, and the version pinned.

### 5. Define failure triage
State how to distinguish environment failures from product failures, who to contact,
and how to record environment defects.

## Output shape
```
## Environment & Data Readiness — <release>
1. Environment map (purpose/version/owner)
2. Configuration matrix
3. Test data plan (create/reset/PII)
4. Readiness checklist (go/no-go)
5. Failure triage & contacts
--- HUMAN REVIEW GATE ---
"Confirm environments and data before execution starts"
```

## Guardrails
- Never use production data or credentials for testing without masking and approval.
- Record the pinned versions; an unpinned environment invalidates results.
- A test that fails due to the environment is an environment issue, not a product bug.

## Human review gate
Report any environment that is not ready and stop before declaring a green cycle.

## References
- The project's provisioning/CI documentation.
