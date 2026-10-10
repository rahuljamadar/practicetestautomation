# Wingify Login Test Cases

Source: [Wingify_Login_TestPlan.md](Wingify_Login_TestPlan.md)

URL: `https://app.wingify.com/#/login`

## Positive Test Cases

| ID | Test Case | Preconditions | Test Steps | Expected Result | Test Data / Oracle |
|---|---|---|---|---|---|
| WLG-POS-001 | Verify login page is displayed | Browser is available | Navigate to the URL | Page title is `Login - Wingify`; email, password, `Sign in`, recovery, alternate sign-in, trial, and legal controls are displayed | Verified through Playwright MCP |
| WLG-POS-002 | Enter a validly shaped email value | Login page is displayed | Fill `Email address` with `test@example.com` | Email field accepts the value and the page remains on the login URL | Observed with Playwright MCP; not a valid-account assertion |
| WLG-POS-003 | Enter a password value | Login page is displayed | Fill `Password` with `Secret123!` | Password field accepts the value and the page remains on the login URL | Observed with Playwright MCP |
| WLG-POS-004 | Activate password visibility control | Password field contains a value | Select `Toggle password visibility` | The control is actionable; the resulting masked or visible state must be recorded | State-change acceptance criterion is not provided |
| WLG-POS-005 | Submit approved valid credentials | Approved valid credentials and post-login oracle are available | Enter the approved email and password; select `Sign in` | The approved post-login URL, title, and landing-page criteria are met | Blocked until credentials and oracle are supplied |
| WLG-POS-006 | Verify Remember me with approved account | Approved valid credentials and persistence requirement are available | Activate `Remember me`; complete login; close and reopen the agreed browser/session | Persistence matches the approved requirement | Blocked until requirement and credentials are supplied |
| WLG-POS-007 | Open password recovery | Login page is displayed and recovery expected behavior is defined | Select `Forgot Password?` | The approved recovery URL, dialog, or workflow is displayed | Blocked until expected behavior is supplied |
| WLG-POS-008 | Open alternate sign-in flows | Expected behavior for each flow is defined | Select Google, SSO, and Passkey separately | Each approved authentication flow opens or starts as specified | Blocked until expected behavior is supplied |
| WLG-POS-009 | Open registration and legal links | Approved destinations are defined | Select `Start a FREE TRIAL`, `Privacy policy`, and `Terms` separately | Each approved destination or behavior is reached | Blocked until destinations are supplied |
| WLG-POS-010 | Verify keyboard accessibility | Accessibility acceptance criteria are defined | Navigate through the page with the keyboard and activate visible controls | Focus order, focus visibility, and activation meet the approved criteria | Blocked until accessibility criteria are supplied |

## Negative Test Cases

| ID | Test Case | Preconditions | Test Steps | Expected Result | Test Data / Oracle |
|---|---|---|---|---|---|
| WLG-NEG-001 | Submit empty login form | Login page is displayed | Select `Sign in` without entering email or password | Message `Your email, password, IP address or location did not match` is displayed; successful login does not occur | Observed with Playwright MCP |
| WLG-NEG-002 | Submit invalid credentials | Login page is displayed; credentials are explicitly designated invalid | Enter invalid email and password; select `Sign in` | The response is recorded and no successful-login assertion is made unless an approved error requirement exists | Blocked until invalid data and oracle are supplied |
| WLG-NEG-003 | Submit an empty email with a password | Login page is displayed | Leave email empty; enter an approved test password; select `Sign in` | The actual response is recorded; exact validation behavior is not asserted | Required-field behavior is unknown |
| WLG-NEG-004 | Submit an email with an empty password | Login page is displayed | Enter an approved test email; leave password empty; select `Sign in` | The actual response is recorded; exact validation behavior is not asserted | Required-field behavior is unknown |
| WLG-NEG-005 | Submit an invalid email format | Login page is displayed | Enter a value explicitly designated invalid by the approved data; enter a password; select `Sign in` | The actual response is recorded; exact format validation behavior is not asserted | Email validation rule is unknown |
| WLG-NEG-006 | Submit an empty email and empty password after clearing fields | Login page is displayed | Clear both fields; select `Sign in` | The observed empty-submit response is displayed, if reproducible | Observed once; repeat in a clean browser context |
| WLG-NEG-007 | Use an unapproved password policy value | Password policy is supplied | Enter a value violating the approved policy and submit | The response matches the approved password-policy requirement | Blocked because password policy is unknown |
| WLG-NEG-008 | Interrupt alternate authentication flow | Alternate flow behavior and interruption handling are supplied | Start Google, SSO, or Passkey authentication; cancel or interrupt it | The interruption response matches the approved requirement | Blocked until flow and oracle are supplied |
| WLG-NEG-009 | Reopen session after unchecked Remember me | Remember-me requirement and approved account are supplied | Ensure `Remember me` is not selected; log in; close and reopen the agreed session | Persistence does not occur if that is the approved requirement | Blocked until requirement and credentials are supplied |
| WLG-NEG-010 | Execute the page at an unsupported or unapproved viewport | Viewport acceptance criteria are supplied | Load the page at the selected viewport | The result is recorded; pass/fail requires approved responsive criteria | Viewport requirements are unknown |

## Execution Rules

- Use accessible Playwright locators observed in the source test plan, such as `getByRole('textbox', { name: 'Email address' })` and `getByRole('button', { name: 'Sign in', exact: true })`.
- Never use real credentials in source control, screenshots, or logs.
- Mark a case `Blocked` when credentials, requirements, supported browsers, viewport sizes, or an expected-result oracle is missing.
- Mark a case `Pass` only when the result is supported by a supplied requirement or direct observation.
- Record the URL, page title, visible response text, and relevant console output for failures and blocked interactions.
- Repeat the observed empty-submit response in a clean browser context before treating it as reproducible.

## Traceability

- Positive cases WLG-POS-001 through WLG-POS-004 trace to WLG-001 through WLG-004 in the test plan.
- Positive cases WLG-POS-005 through WLG-POS-010 trace to WLG-007 through WLG-014 in the test plan.
- Negative cases WLG-NEG-001 and WLG-NEG-006 trace to WLG-005 in the test plan.
- Negative cases WLG-NEG-002 through WLG-NEG-005 trace to WLG-006 and the missing-information section of the test plan.
- Negative cases WLG-NEG-007 through WLG-NEG-010 are conditional extensions of the documented unknowns and remain blocked until their requirements are supplied.