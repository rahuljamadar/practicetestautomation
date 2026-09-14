# Skill Test Plan: VWO (https://vwo.com/)

## 1. Overview
- Requirement ID: TST-VWO-PLAN-001
- Title: End-to-end test plan for VWO website
- Date: 2026-08-16
- Prepared by: Automation Team

## 2. Requirement Summary
- What is the requirement?: Validate core VWO features: auth, signup, campaign lifecycle, visual editor, reporting, integrations, billing, and accessibility.
- Why is it needed?: Ensure platform stability, correctness and regression protection for production-critical flows.
- Who is the stakeholder or user?: Product owners, QA, SRE, and engineering teams.

## 3. Scope
- In scope:
  - Authentication (email/password, SSO if available)
  - Signup/onboarding
  - Campaign creation, edit, publish, pause, archive
  - Visual editor basic operations (edit, save, publish)
  - Reporting generation and export
  - Integrations (webhooks) basic behavior
  - Billing: update payment method validation
  - Accessibility checks on critical pages
- Out of scope:
  - Full third-party integration end-to-end (use sandbox/mocks)
  - Performance/load testing beyond smoke-level checks

## 4. Acceptance Criteria
- Criterion 1: Critical flows (login, create/publish campaign) succeed in supported browsers.
- Criterion 2: Invalid inputs show clear validation errors and no backend changes occur.
- Criterion 3: Accessibility automated checks pass WCAG 2.1 AA assertions on key pages.

## 5. Test Plan
- Test type(s): functional, regression, smoke, API contract, accessibility
- Test environment: staging or test tenant; browsers: Chromium, Firefox, WebKit
- Test data needed:
  - Valid test user accounts (admin/editor/viewer)
  - Invalid credential sets
  - Campaign templates, small and large audience fixtures
  - Mock webhook endpoints
- Dependencies:
  - Staging endpoints and API keys
  - Provisioning API to create/delete test accounts (preferred)

## 6. Test Steps (Per Test Case — use Jira format: Test case id, description, steps, expected result)

---

Test case id: TST-VWO-AUTH-001-FUNC
Description: Login with valid credentials
Steps:
1. Navigate to login page
2. Enter valid email and password
3. Click Login
Expected result:
1. User is redirected to Dashboard
2. Session cookie or auth token is present

---

Test case id: TST-VWO-AUTH-002-FUNC
Description: Login with invalid password
Steps:
1. Navigate to login page
2. Enter valid email and incorrect password
3. Click Login
Expected result:
1. Error message displayed indicating invalid credentials
2. No session cookie or token created

---

Test case id: TST-VWO-SIGN-001-FUNC
Description: Signup with valid data and email verification flow
Steps:
1. Navigate to signup page
2. Fill required fields (email, password, org name)
3. Accept terms and submit
4. Open verification email and click verification link
Expected result:
1. Account created and verification email sent
2. After clicking verification, account is activated and user can login

---

Test case id: TST-VWO-CAMP-001-SMOKE
Description: Create minimal campaign and publish (smoke)
Steps:
1. Login as a user with create permission
2. Navigate to Campaigns → Create New
3. Enter campaign name, set URL, add one variation
4. Allocate traffic and click Publish
Expected result:
1. Campaign state becomes `running` or `published`
2. Campaign appears in Dashboard with correct status

---

Test case id: TST-VWO-CAMP-002-REG
Description: Edit campaign variations and save as draft
Steps:
1. Open existing draft campaign
2. Modify variation details (name, content)
3. Save as draft
Expected result:
1. Changes are saved to campaign draft
2. No publish action occurs

---

Test case id: TST-VWO-EDIT-001-REG
Description: Visual Editor — change text content, undo, save and publish
Steps:
1. Open visual editor for a campaign
2. Select an element and change text
3. Use undo to revert the change
4. Re-apply change and save, then publish
Expected result:
1. Undo restores original text
2. After publish, published variation displays updated text

---

Test case id: TST-VWO-REPORT-001-FUNC
Description: Generate report for date range and export CSV
Steps:
1. Navigate to Reports
2. Select date range and segmentation
3. Run report and click Export CSV
Expected result:
1. Report results display and match expected counts
2. CSV file is downloaded and contains correct headers and rows

---

Test case id: TST-VWO-INT-001-API
Description: Webhook delivery with retry on 5xx from endpoint
Steps:
1. Configure webhook to point to mock endpoint that returns 500
2. Trigger event that invokes webhook
3. Verify retry behavior and final logged status
Expected result:
1. System retries per retry policy and logs attempts
2. Failure is recorded if endpoint never succeeds

---

Test case id: TST-VWO-BILL-001-FUNC
Description: Update payment method with invalid card number
Steps:
1. Navigate to Billing → Payment methods
2. Enter invalid card number and submit
Expected result:
1. Validation error displayed; payment method not updated

---

Test case id: TST-VWO-A11Y-001-ACC
Description: Keyboard navigation through Visual Editor toolbar
Steps:
1. Open Visual Editor
2. Use Tab/Shift+Tab to navigate toolbar controls
3. Activate key controls with Enter/Space
Expected result:
1. All toolbar controls are reachable by keyboard
2. Controls have ARIA labels or roles for screen readers

---

Test case id: TST-VWO-AUTH-003-EDGE
Description: Session expiry mid-publish (edge case)
Steps:
1. Start publish operation
2. Expire session token (simulate or wait)
3. Continue publish action
Expected result:
1. Operation fails gracefully and prompts user to re-authenticate or resume

---

Test case id: TST-VWO-CAMP-EDGE-001-EDGE
Description: Traffic allocation boundary values (0%, 100%)
Steps:
1. Create campaign and set traffic allocation to 0%
2. Verify behavior; set to 100% and verify behavior
Expected result:
1. 0% allocation does not deliver traffic to variation; 100% sends all traffic to variation

---

## 7. Expected Results
- See per-test Expected result sections above.

## 8. Notes and Observations
- Use API-backed setup for speed in automation when possible.
- Tag DOM elements with `data-test-id` for stable selectors.

## 9. Real-Time Usage Guidance
- Copy this template into new test notes for each new requirement and follow the Jira format (Test case id, description, steps, expected result).
