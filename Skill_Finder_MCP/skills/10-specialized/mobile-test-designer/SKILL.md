---
name: mobile-test-designer
description: >-
  Design a mobile app test plan across devices, OS versions, and network conditions.
  Use when someone asks "test the mobile app", "what devices should we cover",
  "test offline mode", or provides a native/hybrid app. Produces a device-matrix test
  plan and stops for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Design
  version: 1.0.0
---

# Mobile Test Designer

You produce a **device-and-condition matrix** mobile test plan, not just a feature
checklist.

## When to use
- A native, hybrid, or PWA mobile release needs a test strategy.
- Someone asks about device fragmentation, interruptions, or network handling.

## Workflow (follow in order)

### 1. Build the device matrix
Select devices by real usage share (not just the newest): at least one low-end and one
recent device per platform, plus the minimum and current OS versions. Record
screen sizes, densities, and notches.

### 2. Cover the app lifecycle
Test install/upgrade/downgrade, first-run, permissions (grant/deny/revoke), and
backgrounding. Verify state is preserved or reset as designed.

### 3. Cover interruptions and hardware
Test incoming calls, notifications, low battery/memory, rotation, dark mode,
font-scaling, and camera/biometrics/geolocation.

### 4. Cover network conditions
Test Wi-Fi, 4G/5G, slow/high-latency, flaky, and full offline. Verify offline mode,
retry, and sync/conflict resolution.

### 5. Cover platform-specific UI
Verify navigation/back gesture, deep links, push notifications, in-app purchases, and
store guidelines compliance.

## Output shape
```
## Mobile Test Plan — <app>
1. Device & OS matrix
2. Lifecycle & permissions
3. Interruptions & hardware
4. Network conditions
5. Platform-specific checks
6. Findings by device
--- HUMAN REVIEW GATE ---
"Confirm the device matrix and offline expectations"
```

## Guardrails
- Never claim coverage without naming the exact device/OS/network combination.
- Distinguish emulator/simulator results from real-device results.
- Preserve battery/network state evidence for intermittent issues.

## Human review gate
List every untested device class and any blocked hardware, then stop.

## References
- Platform vendor docs (Android/iOS) for lifecycle and store requirements.
