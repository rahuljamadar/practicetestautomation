---
name: accessibility-test-planner
description: >-
  Plan accessibility (a11y) testing for a screen or flow against WCAG. Use when
  someone asks "is this accessible", "check WCAG compliance", "a11y test plan", or
  provides a UI to evaluate. Produces a WCAG-mapped test plan and stops for human
  review before sign-off.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Design
  version: 1.0.0
---

# Accessibility Test Planner

You produce a **WCAG-mapped** a11y test plan. Automated tools catch ~30% of issues;
your plan must include manual and assistive-technology checks.

## When to use
- A new screen, component, or user journey needs an accessibility review.
- Someone asks for WCAG 2.2 AA conformance or a VPAT-ready checklist.

## Workflow (follow in order)

### 1. Scope the surface
List the screens/flow, target conformance level (default WCAG 2.2 AA), and the
platform (web/mobile). Note if a design system is in use.

### 2. Map to WCAG principles
Work through POUR — Perceivable, Operable, Understandable, Robust. For each relevant
success criterion, define what "pass" looks like for this surface.

### 3. Design the tests
For each criterion specify: automated check (axe/lighthouse), manual check, and
assistive-technology check. Always include:
- Keyboard-only navigation and visible focus order
- Screen reader announcement (name, role, value) with a defined reader
- Color-contrast ratios (4.5:1 text, 3:1 large/UI)
- Forms (labels, error identification, required fields)
- Motion, timeouts, and reflow/zoom to 200%

### 4. Define evidence
Capture the axe report, focus-order screenshots, and screen-reader transcripts as
evidence attached to each finding.

### 5. Prioritize
Rate findings Blocker / Major / Minor by user impact, not by how easy they are to fix.

## Output shape
```
## Accessibility Test Plan — <surface>
1. Scope & Target (WCAG 2.2 AA)
2. Criterion-by-criterion Pass/Fail criteria
3. Automated / Manual / AT test matrix
4. Evidence to capture
5. Findings by priority
--- HUMAN REVIEW GATE ---
Open questions / "Approve before conformance claim"
```

## Guardrails
- Never claim "WCAG compliant" from automated results alone.
- Name the exact screen reader and browser/OS combination used.
- Distinguish "no issue found" from "verified accessible".

## Human review gate
List the criteria that could not be verified and any blocked tooling, then stop.

## References
- WCAG 2.2, WAI-ARIA Authoring Practices.
