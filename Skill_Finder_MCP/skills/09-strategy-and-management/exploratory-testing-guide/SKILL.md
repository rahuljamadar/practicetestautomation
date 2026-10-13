---
name: exploratory-testing-guide
description: >-
  Plan and run time-boxed exploratory testing sessions. Use when someone asks "do some
  exploratory testing", "find bugs we haven't scripted", "session-based test a
  feature", or provides a feature to investigate. Produces a charter, session notes,
  and findings, and stops for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Execution
  version: 1.0.0
---

# Exploratory Testing Guide

You run **session-based, charter-driven** exploration. You report what you actually
observed, separating confirmed bugs from suspicions.

## When to use
- Requirement pages are thin and scripted tests won't cover the risk well.
- A diverse, heuristic-driven pass is needed before or after scripted testing.

## Workflow (follow in order)

### 1. Write a charter
Use the form: `Explore <target> with <resources> to discover <information>.` Add a
time box (default 90 minutes) and the risk area driving the session.

### 2. Choose heuristics
Select techniques to guide discovery: SFDIPOT, FEW HICCUPPS (consistency heuristics),
CRUD, boundary, and persona touring. State which you are using and why.

### 3. Execute and take notes
Log in three streams: what you did, what you observed, and the questions that arose.
Capture evidence (screenshots, requests) for anything suspicious.

### 4. Triage findings
Classify each finding: confirmed bug (with repro), suspected bug (needs
verification), question, or test-idea. Do not report a suspicion as a defect.

### 5. Summarize and debrief
Produce a session report: charter, duration, coverage, findings, and follow-ups.

## Output shape
```
## Exploratory Session — <charter>
1. Charter & time box
2. Heuristics used
3. Session notes (did / observed / questions)
4. Findings (confirmed / suspected / ideas)
5. Coverage & follow-ups
--- HUMAN REVIEW GATE ---
"Confirm findings before filing defects"
```

## Guardrails
- Never file a suspected bug as confirmed without a reproduction.
- Stay within the time box; log new ideas rather than chasing them.
- Preserve evidence for every confirmed finding.

## Human review gate
Present suspected findings and unverified repro steps for review before filing.

## References
- Session-Based Test Management; heuristics: SFDIPOT, FEW HICCUPPS.
