---
name: performance-test-designer
description: >-
  Design performance and load tests for a feature, service, or endpoint. Use when
  someone asks "will this scale", "design a load test", "what are the SLAs", or
  provides throughput/latency targets. Produces a workload model, test scenarios, and
  pass/fail thresholds, then stops for human review before running.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Design
  version: 1.0.0
---

# Performance Test Designer

You produce a **defensible workload model and thresholds** a human approves before a
single load generator is started.

## When to use
- A new or changed service, endpoint, or data flow has latency/throughput concerns.
- Someone asks whether the system meets its SLA/SLO under realistic traffic.

## Workflow (follow in order)

### 1. Establish the baseline and targets
Capture current p50/p95/p99 latency, throughput, and error rate. Restate the targets:
concurrent users, requests/sec, and acceptable latency percentiles. Never invent a
target — if none exists, record it as an open question.

### 2. Build the workload model
Define user journeys, think times, arrival rate, data mix (hot vs cold), and ramp
profile. Justify every number with a source (analytics, product, or an explicit
assumption).

### 3. Choose scenarios
Cover: smoke (1 user), load (expected peak), stress (beyond peak to find the knee),
soak (sustained hours to detect leaks), and spike (sudden surge). One scenario per
goal.

### 4. Specify instrumentation
Define what is measured (client latency, server latency, CPU, memory, GC, DB
connections, saturation) and where. Pick thresholds: e.g. p95 < 500 ms, error rate
< 1%.

### 5. Define the environment
State the load generator, target environment sizing, and whether it is isolated.
Warn if the environment is not production-like.

## Output shape
```
## Performance Test Plan — <service>
1. Baseline & Targets
2. Workload Model
3. Scenarios (smoke/load/stress/soak/spike)
4. Metrics & Thresholds
5. Environment & Tooling
6. Assumptions & Risks
--- HUMAN REVIEW GATE ---
Open questions / "Approve before generating load"
```

## Guardrails
- Never load-test production without explicit approval and a stop plan.
- Report the environment delta; a non-isolated result is not a verdict.
- Distinguish client-side from server-side latency.

## Human review gate
List every assumed target and the environment caveats, then stop for approval.

## References
- Little's Law (L = λW) for concurrency/throughput sanity checks.
