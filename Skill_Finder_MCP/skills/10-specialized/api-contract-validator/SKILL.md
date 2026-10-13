---
name: api-contract-validator
description: >-
  Validate that an API honours its contract (schema, status codes, versioning). Use
  when someone asks "does the API match the spec", "validate the OpenAPI schema",
  "test contract compatibility", or provides an OpenAPI/Swagger file or endpoint.
  Produces a contract test plan and stops for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Design
  version: 1.0.0
---

# API Contract Validator

You validate the **contract** an API promises, independent of UI behaviour. The
specification is the source of truth; the implementation must conform to it.

## When to use
- An OpenAPI/Swagger or similar spec exists and must match the live API.
- A producer/consumer change risks breaking integrators.

## Workflow (follow in order)

### 1. Capture the contract
Obtain the spec (OpenAPI, GraphQL SDL, or documented JSON schema). Record its version
and the versioning policy (URL, header, or media type).

### 2. Validate structure
For every endpoint check: request/response schema (types, required fields,
additional properties), enum values, formats, and nullability. Flag
implementation-drift from the spec.

### 3. Validate behaviour
Verify status codes (success, 4xx, 5xx), error body shape, pagination, filtering/sort
parameters, idempotency of PUT/DELETE, and auth/permission responses.

### 4. Check compatibility
Compare the new contract against the previous version. Classify changes as
breaking / non-breaking (removed fields, type changes, new required params are
breaking; additive optional fields are not).

### 5. Define consumer-driven checks
Where consumers exist, capture their expectations and assert compatibility as a gate.

## Output shape
```
## API Contract Validation — <service>
1. Contract source & version
2. Structural validation results
3. Behavioural validation results
4. Compatibility classification (breaking vs not)
5. Consumer expectations
--- HUMAN REVIEW GATE ---
"Confirm breaking-change classification before release"
```

## Guardrails
- The spec, not the implementation, is the baseline; report both when they diverge.
- Never call a live third-party API without permission or rate-limit awareness.
- Classify every change; an unclassified removal is a release risk.

## Human review gate
List every breaking change and any spec ambiguity, then stop for sign-off.

## References
- OpenAPI Specification; semantic versioning for APIs.
