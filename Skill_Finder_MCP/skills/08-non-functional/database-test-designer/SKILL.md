---
name: database-test-designer
description: >-
  Design database and data-integrity tests. Use when someone asks "how do we test the
  migration", "verify the schema/data", "test the stored procedures", or provides a
  data model, SQL migration, or data flow. Produces a data-layer test plan and stops
  for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Design
  version: 1.0.0
---

# Database Test Designer

You design **data-integrity-first** database tests. You never run destructive SQL
against non-test environments.

## When to use
- A schema change, migration, ETL job, or stored procedure is being delivered.
- Someone asks to verify data integrity, constraints, or transactions.

## Workflow (follow in order)

### 1. Understand the data model
Map tables, keys, relationships, constraints, and indexes touched by the change.
Identify the volume and sensitivity (PII) of the data.

### 2. Design schema tests
Verify column types, nullability, defaults, primary/foreign keys, unique constraints,
and check constraints behave as specified. Confirm indexes exist for expected queries.

### 3. Design migration tests
For every migration verify: forward application, rollback, idempotency, handling of
existing rows, and behaviour on a populated copy of production-like data. Never run
against production.

### 4. Design data-integrity and transaction tests
Cover CRUD paths, referential integrity (no orphans), cascade behaviour, concurrent
updates, and ACID guarantees (commit/rollback boundaries). Include boundary and
empty-data cases.

### 5. Design query and performance checks
Verify correctness of key queries and, where relevant, that plan/index usage avoids
full scans on large tables.

## Output shape
```
## Database Test Plan — <change>
1. Data Model & Scope
2. Schema / Constraint tests
3. Migration tests (up/rollback/idempotent)
4. Integrity & Transaction tests
5. Query & Index checks
6. Test data & environment
--- HUMAN REVIEW GATE ---
Open questions / "Approve before touching any database"
```

## Guardrails
- Never run destructive or migration SQL outside an isolated test database.
- Use synthetic data; mask any PII copied from production.
- Record the exact schema version before and after.

## Human review gate
List the environments and data-sets you intend to use and any destructive step, then
stop for explicit approval.

## References
- ACID properties; the project's migration tooling docs.
