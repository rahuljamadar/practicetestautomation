# Ricepot Test Plan — Practice Test Automation Login (End-to-End UI)

## 1. Overview
- Requirement ID: E2E-LOGIN-001
- Title: End-to-End UI validation of the Practice Test Automation login flow
- Application: https://practicetestautomation.com/practice-test-login/
- Date: 2026-08-09
- Prepared by: QA / Automation team
- Goal: Validate the complete login user journey — landing on the login page, submitting credentials, reaching the success page, and logging out — plus all negative paths, using Playwright with the Page Object Model (POM).

## 2. Objective
Prove the login feature works end to end as a user experiences it:
- The login page renders with all required fields and the Submit button.
- Valid credentials log the user in and land on the success page with the success message and Log out button visible.
- Logging out returns the user to the login page.
- Invalid and empty credentials show the correct inline error messages and keep the user on the login page.
- The same behavior holds on the supported browser matrix (Chromium and Firefox).

## 3. Requirement Summary
- What: An automated end-to-end UI test suite for the login flow at practicetestautomation.com.
- Why: To catch regressions in the login journey before they reach real users and to document the expected UI behavior.
- Who: QA team (author), developers (consumers of the failure report), stakeholders (sign-off on quality).

## 4. Scope
In scope:
- Login page rendering (username field, password field, Submit button).
- Positive login: valid credentials → success page (URL, success message, Log out button).
- Logout: click Log out → back on the login page.
- Negative login: invalid username, invalid password, empty username, empty password.
- Error message assertions for each negative case.
- UI state verification using Playwright auto-waiting and assertions (no fixed sleeps).

Out of scope:
- API-level testing (see Ricepot.md API plan).
- Non-login pages and other site functionality.
- Responsiveness on tablet/mobile viewports (desktop viewport only).
- Performance, load, security, and backup/recovery testing.
- Accessibility and localization testing.

## 5. Acceptance Criteria
- Criterion 1: A user with valid credentials reaches the success page (`/logged-in-successfully/`) and sees the success message and Log out button.
- Criterion 2: Clicking Log out returns the user to the login page.
- Criterion 3: Invalid or empty credentials show the exact expected error text and never reach the success page.
- Criterion 4: All scenarios pass on both Chromium and Firefox.
- Criterion 5: Test runs produce an HTML report and on-failure screenshots/videos/traces.

## 6. Test Environment
- Browsers: Chromium (Chrome channel) and Firefox (local executable) — configured in `playwright.config.js`.
- Execution: headless, 1280x800 viewport, local machine (Node.js + Playwright).
- Base URL: `https://practicetestautomation.com` (overridable via `BASE_URL`).
- Test data: hardcoded in `data/loginData.js` (valid: `student` / `Password123`; invalid: `incorrectUser` / `incorrectPassword`).
- Dependencies: Playwright, Node.js, page objects in `pages/loginPage.js`.

### Environment Matrix
| Scenario | Chromium | Firefox |
| --- | --- | --- |
| Positive login | Yes | Yes |
| Logout | Yes | Yes |
| 4 negative cases | Yes | Yes |

## 7. Inclusions (Test Scenarios and Cases)

### 7.1 Positive Flow (End-to-End)
- TC-LOGIN-001 Positive login navigates to the success page
  - Steps:
    1. Open the login URL.
    2. Assert URL matches `/practice-test-login/` and username field is visible.
    3. Enter valid username and password.
    4. Click Submit.
  - Expected: URL becomes `/logged-in-successfully/`, success message visible, Log out button visible.

- TC-LOGIN-002 Logout returns to the login page
  - Steps:
    1. Log in with valid credentials.
    2. Assert success page is shown.
    3. Click the Log out button.
  - Expected: URL returns to `/practice-test-login/` and the login form is visible again.

### 7.2 Negative Flow (Error Handling)
- TC-LOGIN-003 Invalid username
  - Steps: enter invalid username + valid password, Submit.
  - Expected: error box visible with text "Your username is invalid!".
- TC-LOGIN-004 Invalid password
  - Steps: enter valid username + invalid password, Submit.
  - Expected: error box visible with text "Your password is invalid!".
- TC-LOGIN-005 Empty username
  - Steps: leave username blank + valid password, Submit.
  - Expected: error box visible with text "Your username is invalid!".
- TC-LOGIN-006 Empty password
  - Steps: enter valid username + blank password, Submit.
  - Expected: error box visible with text "Your password is invalid!".

### 7.3 Assertion Strategy (Playwright Waits)
- Use `expect(...).toBeVisible()`, `toHaveURL(regex)`, and `toContainText(...)` for built-in auto-waiting.
- Never use fixed sleeps; rely on Playwright's action and expectation timeouts (see `playwright.config.js`).

## 8. Test Data
- Valid credentials: username `student`, password `Password123`.
- Invalid username: `incorrectUser`.
- Invalid password: `incorrectPassword`.
- Expected error texts: "Your username is invalid!" and "Your password is invalid!".
- Locators (via `data/loginData.js` and `pages/loginPage.js`): `[name="username"]`, `[name="password"]`, button with text "Submit", `#error`, success heading/paragraph, Log out link.

## 9. Test Strategy
- Page Object Model to encapsulate login page behavior and locators.
- Test design techniques: Equivalence Class Partitioning (valid vs invalid credentials), Error Guessing (empty fields), State Transition Testing (logged out → logged in → logged out).
- Positive and negative cases run fully parallel; retries configured (1 locally, 2 in CI).
- Smoke-first approach: run the positive login and one negative case first; if those pass, run the full suite.

### Testing Procedure
1. Run smoke tests (TC-LOGIN-001, TC-LOGIN-003) to verify essential functionality.
2. If smoke tests fail, treat the build as unstable and re-check before deeper testing.
3. Execute the full suite on both browsers.
4. Report defects in the tracking tool and share daily status updates.

## 10. Defect Reporting Procedure
- Criteria: deviation from expected results in Section 7, broken locators, unexpected navigation.
- Template: reproduction steps, expected vs actual, screenshot/video (Playwright captures on failure), severity, priority.
- Track in the defect tracking tool (e.g., JIRA); assign owner per defect process.

## 11. Entry and Exit Criteria
### Entry Criteria
- Node.js and Playwright installed; `npx playwright install` completed.
- Application URL accessible and credentials available.
- Test scenarios signed off.

### Exit Criteria
- All tests pass on Chromium and Firefox locally.
- Any defects logged, triaged, and resolved or documented.
- Test report generated (`npm run test:report`) and results summarized.

## 12. Risks and Mitigations
- Risk: Page HTML changes (locators break)
  - Mitigation: Resilient locators in `loginData.js`/`loginPage.js`; update and rerun on change.
- Risk: Network or site downtime
  - Mitigation: Retry later or run against a stable environment via `BASE_URL`.
- Risk: Firefox executable path unavailable
  - Mitigation: Override via `FIREFOX_EXECUTABLE_PATH` or scope to Chromium.

## 13. Test Schedule and Deliverables
- Test Plan creation → Test case creation → Test case execution → Summary report.
- Deliverables: `playwright.config.js`, `pages/loginPage.js`, `data/loginData.js`, `tests/login.spec.js`, `TestPlan.md`, README, HTML report.

## 14. Approvals
- Test plan reviewed by QA lead before execution.
- Test scenarios and cases signed off before test execution.
- Summary reports sent for client approval before closure.
