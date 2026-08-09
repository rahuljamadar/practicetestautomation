# Test Plan for Practice Test Automation Login

## 1. Overview
- Application: Practice Test Automation login page
- URL: https://practicetestautomation.com/practice-test-login/
- Goal: Validate positive and negative login scenarios using Playwright with POM and an industry-standard JavaScript test structure.

## 2. Objective
Ensure the login page functions correctly, handles valid credentials, and returns proper error messages for invalid credentials.
- Test credentials: Username `student`, Password `Password123`

## 3. Scope
In scope:
- Positive login flow
- Negative login flows for invalid username and invalid password
- Empty credentials handling
- Verification of success page and logout button on successful login
- Verification of specific error messages for invalid credentials

Out of scope:
- API-level testing
- Non-login pages
- UI responsiveness or browser compatibility beyond standard Chrome headless execution

## 4. Inclusions
- Valid login scenario
- Invalid username scenario
- Invalid password scenario
- Empty username scenario
- Empty password scenario

## 5. Test Environments
- Local machine using Playwright's Chromium headless browser
- Node.js environment with Playwright dependencies

## 6. Test Strategy
- Use Page Object Model to encapsulate page behavior
- Use Playwright locators with default XPath statements only
- Avoid `Thread.sleep` equivalent; use Playwright waiting mechanisms
- Execute tests in parallel where possible

## 7. Test Schedule
- Framework setup: 1 day
- Page object and test script creation: 1 day
- Review and validation: 1 day

## 8. Deliverables
- `playwright.config.js`
- `pages/loginPage.js`
- `tests/login.spec.js`
- `TestPlan.md`
- `README.md` and framework structure

## 9. Entry and Exit Criteria
Entry criteria:
- Test environment configured with Node.js and Playwright
- Application URL accessible
- Required credentials available

Exit criteria:
- All tests pass in the local environment
- Any defects logged and addressed
- Test results documented

## 10. Risks and Mitigations
- Risk: Page HTML changes
  - Mitigation: Use resilient XPath locators and update page objects
- Risk: Network or site downtime
  - Mitigation: Retry later or run against a stable copy of the site

## 11. Missing Requirements
- No explicit requirement for browser cross-compatibility testing
- No requirement for performance or load testing
- No back-end or API validation details
- No test data management strategy beyond hardcoded credentials
- No explicit requirement for user logout flow validation
- No requirement for accessibility or localization testing

## 12. Approvals
- Test Plan review by QA lead
- Approval before execution
