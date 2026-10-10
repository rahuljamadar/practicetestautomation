# Test Plan - User Login

**Environment:** Environment: local

## 1. Objective
Validate that the feature meets the stated requirement and acceptance criteria in the target environment.

## 2. Scope
**In Scope:** User Login
**Out of Scope:** Performance and load testing, Security penetration testing, Cross-browser visual regression

## 3. Assumptions / Dependencies
- The requirement text is the source of truth.
- No business rules are assumed beyond what is stated.
- Acceptance criteria were provided and mapped to test cases.
- Stated constraints are respected during execution.

## 4. Test Strategy
Deterministic generation from the stated requirement: positive cases per stated behavior, negative case for invalid input, and boundary case when numeric limits are present.

## 5. Test Data Requirements
- Environment: local

## 6. Risks / Constraints
- Unstated business rules may be missed.

## 7. Entry Criteria
- Requirement text is validated and non-empty.
- Target environment is available.

## 8. Exit Criteria
- All test cases are executed and reviewed.
- All defects are logged or explicitly accepted as risks.

## 9. Detailed Test Cases

| ID | Title | Priority | Type |
|----|-------|----------|------|
| TC-01 | Verify: Users must be able to log in with their email and password. | High | Positive |
| TC-02 | Verify: The system must lock the account after 5 failed attempts. | High | Positive |
| TC-03 | Acceptance: Successful login redirects to the dashboard | High | Positive |
| TC-04 | Negative: invalid or incomplete input is rejected | Medium | Negative |
| TC-05 | Boundary: numeric limits stated in the requirement | Medium | Boundary |

### TC-01 - Verify: Users must be able to log in with their email and password.

- **Scenario:** Positive scenario derived from the stated requirement.
- **Steps:**
  1. Open the feature in the target environment.
  1. Execute the behavior described: Users must be able to log in with their email and password.
  1. Observe the result.
- **Expected Result:** The system behaves exactly as stated in the requirement.
- **Priority:** High | **Type:** Positive

### TC-02 - Verify: The system must lock the account after 5 failed attempts.

- **Scenario:** Positive scenario derived from the stated requirement.
- **Steps:**
  1. Open the feature in the target environment.
  1. Execute the behavior described: The system must lock the account after 5 failed attempts.
  1. Observe the result.
- **Expected Result:** The system behaves exactly as stated in the requirement.
- **Priority:** High | **Type:** Positive

### TC-03 - Acceptance: Successful login redirects to the dashboard

- **Scenario:** Acceptance criterion verification.
- **Steps:**
  1. Reproduce the acceptance criterion context.
  1. Check: Successful login redirects to the dashboard
  1. Record the actual result.
- **Expected Result:** The acceptance criterion is fully met.
- **Priority:** High | **Type:** Positive

### TC-04 - Negative: invalid or incomplete input is rejected

- **Scenario:** User provides empty, placeholder, or malformed input.
- **Steps:**
  1. Submit an empty requirement.
  1. Submit a placeholder requirement.
  1. Submit a valid requirement.
- **Expected Result:** Empty and placeholder inputs are rejected with a clear message; valid input proceeds to plan generation.
- **Priority:** Medium | **Type:** Negative

### TC-05 - Boundary: numeric limits stated in the requirement

- **Scenario:** Test values at the stated numeric boundary.
- **Steps:**
  1. Identify the numeric limit in the requirement.
  1. Test at the limit, just below it, and just above it.
- **Expected Result:** Values at and below the limit succeed; values above the limit are handled gracefully per the stated rule.
- **Priority:** Medium | **Type:** Boundary
