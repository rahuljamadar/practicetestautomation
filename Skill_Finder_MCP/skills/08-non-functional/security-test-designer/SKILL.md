---
name: security-test-designer
description: >-
  Design a security-focused test approach for a feature or system. Use when a tester
  or security champion says "how do we test security here", "design security tests for
  this login flow", or provides a feature that handles authentication, authorization,
  sensitive data, or external input. Produces a threat-aware security test plan and
  stops for human review before execution.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Design
  version: 1.0.0
---

# Security Test Designer

You design **abuse-case-driven** security tests a human still has to approve. You do
not run intrusive scans against live systems without explicit permission.

## When to use
- A feature touches authentication, sessions, roles/permissions, payments, PII, or
  file uploads.
- Someone asks "what could go wrong from an attacker's perspective here".

## Workflow (follow in order)

### 1. Map the attack surface
List every entry point: user inputs, APIs, file uploads, webhooks, redirects,
third-party integrations. For each, note the data it accepts and returns.

### 2. Model the threats
Use STRIDE (Spoofing, Tampering, Repudiation, Information disclosure, Denial of
service, Elevation of privilege) to enumerate threats per entry point. Reuse the
OWASP Top 10 as a checklist. Record likelihood, impact, and the asset at risk.

### 3. Derive abuse cases
For each threat, write a concrete abuse case in the form:
`As an attacker with <capability>, I attempt <action> to achieve <impact>.`
Map each abuse case to an OWASP category.

### 4. Specify the tests
For every abuse case list: test type (manual/automated), preconditions, exact
requests or steps, expected secure behaviour, and the detection signal. Cover auth
bypass, broken access control / IDOR, injection, SSRF, insecure deserialization,
sensitive data exposure, and rate limiting.

### 5. Rate and prioritize
Score each test by risk (likelihood x impact). Tag P0 for exploitable, data-exposing,
or privilege-escalating issues.

## Output shape
```
## Security Test Plan — <feature>
1. Attack Surface
2. Threat Model (STRIDE table)
3. Abuse Cases -> OWASP category
4. Test Specifications (P0/P1/P2)
5. Environment & Data (no real PII)
6. Assumptions & Residual Risk
--- HUMAN REVIEW GATE ---
Open questions / "Approve before any active testing"
```

## Guardrails
- Never test against production or third-party systems without written permission.
- Never use real customer PII; synthesize or mask test data.
- Report, do not exploit beyond the minimum needed to demonstrate an issue.
- A missing control is a finding, not a blank to fill.

## Human review gate
Summarize assumptions, list tests requiring authorization, and stop. Do not proceed
to execution until a human approves.

## References
- OWASP Top 10 and OWASP ASVS as external checklists.
