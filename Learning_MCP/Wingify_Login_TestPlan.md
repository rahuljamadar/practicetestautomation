# Wingify Login Test Plan

## Verified Facts:

- URL: `https://app.wingify.com/#/login`
- Page title: `Login - Wingify`
- The page exposes an application main content region.
- The page exposes an email field named `Email address` with placeholder `Enter email ID`.
- The page exposes a password field named `Password` with placeholder `Enter password`.
- The page exposes a `Toggle password visibility` button.
- The page exposes a `Forgot Password?` button.
- The page displays `Remember me`.
- The page exposes a `Sign in` button.
- The page exposes `Sign in with Google`, `Sign in using SSO`, and `Sign in with Passkey` buttons.
- The page displays `Or` between the primary and alternate sign-in controls.
- The page displays `New to Wingify?`.
- The page exposes a `Start a FREE TRIAL` link.
- The page exposes `Privacy policy` and `Terms` links.
- The page displays `Agentic Experience Optimization Platform`.
- The page displays the heading `Make every digital experience relevant`.
- Playwright MCP observed the message `Your email, password, IP address or location did not match` after selecting `Sign in` with empty fields.
- Playwright MCP filled `test@example.com` and `Secret123!` into the email and password fields without leaving the page.
- Playwright MCP selected the password visibility control without leaving the page.

## Missing / Unknown Information:

- Valid login credentials are not provided.
- Expected post-login URL, page title, and authenticated landing page are not provided.
- Required-field validation rules and message text are not specified.
- Email-format validation rules and message text are not specified.
- Password policy is not specified.
- The persistence behavior of `Remember me` is not specified.
- The expected behavior of Google, SSO, and Passkey sign-in is not specified.
- The expected behavior of `Forgot Password?` is not specified.
- The expected destinations for the trial, privacy, and terms links are not requirements; their observed hrefs were not used as pass criteria.
- Browser support, viewport requirements, accessibility conformance target, performance targets, and test environment are not provided.
- The meaning of the observed console errors and warnings is not determined.

## Generated Output:

### Scope

Validate the observable login-page UI and the login interaction using Playwright. Do not assert unspecified backend outcomes. Use only approved test credentials when they are supplied.

### Preconditions and Test Data

1. The supplied URL is reachable.
2. A supported browser and Playwright environment are available.
3. For successful-login testing, valid credentials and expected post-login behavior must be supplied. Otherwise, report `Insufficient information to determine.`
4. Use a dedicated non-production account for credential-based tests.

### Test Cases

| ID | Scenario | Steps | Expected Result | Status Basis |
|---|---|---|---|---|
| WLG-001 | Verify login page loads | Navigate to the supplied URL | Page title is `Login - Wingify`; email, password, `Sign in`, alternate sign-in controls, recovery control, trial link, legal links, and right-panel copy are available as listed in Verified Facts | Observable via Playwright MCP |
| WLG-002 | Verify email field accepts input | Fill `Email address` with `test@example.com` | The field accepts the supplied value and the page remains on the login URL | Observed with Playwright MCP |
| WLG-003 | Verify password field accepts input | Fill `Password` with `Secret123!` | The field accepts the supplied value and the page remains on the login URL | Observed with Playwright MCP |
| WLG-004 | Verify password visibility control is actionable | Fill the password field; select `Toggle password visibility` | The control is selectable. Whether the password changes between masked and visible states is not specified; verify and record the actual result | Control observed and selected; outcome not asserted |
| WLG-005 | Submit empty login form | Select `Sign in` without entering credentials | The observed message `Your email, password, IP address or location did not match` is displayed; no successful-login assertion is made | Observed with Playwright MCP |
| WLG-006 | Submit supplied invalid credentials | Enter credentials explicitly designated as invalid; select `Sign in` | Record the displayed response. Exact error text and navigation are unspecified, so pass/fail requires an approved requirement | Test data and oracle required |
| WLG-007 | Submit valid credentials | Enter approved valid credentials; select `Sign in` | The supplied expected post-login URL, title, and landing-page criteria are satisfied | Credentials and oracle required |
| WLG-008 | Verify Remember me behavior | Select or activate `Remember me`; complete an approved login; close and reopen the browser/session according to the agreed test environment | Persistence behavior is verified against an approved requirement | Requirement and credentials required |
| WLG-009 | Verify password recovery entry point | Select `Forgot Password?` | The resulting page, dialog, URL, and validation behavior are recorded; pass/fail requires the specified expected behavior | Expected behavior required |
| WLG-010 | Verify alternate authentication entry points | Select Google, SSO, and Passkey controls separately | Each control is actionable and its resulting flow is recorded; pass/fail requires the specified expected behavior | Expected behavior required |
| WLG-011 | Verify registration and legal links | Select `Start a FREE TRIAL`, `Privacy policy`, and `Terms` separately | Each link opens the approved destination or behavior | Destination requirements required |
| WLG-012 | Verify keyboard access | Use keyboard navigation from the page start and activate the visible controls | Focus order, focus visibility, and activation behavior are recorded; accessibility acceptance criteria are not provided | Accessibility oracle required |
| WLG-013 | Verify responsive presentation | Execute the page at approved desktop and mobile viewport sizes | Layout remains usable and all required controls remain available | Viewport requirements required |
| WLG-014 | Verify browser compatibility | Execute the approved suite in each supported browser | All applicable cases pass in each supported browser | Browser matrix required |

### Playwright Locator Guidance

Use the accessible names observed by Playwright MCP where possible:

- `getByRole('textbox', { name: 'Email address' })`
- `getByRole('textbox', { name: 'Password' })`
- `getByRole('button', { name: 'Sign in', exact: true })`
- `getByRole('button', { name: 'Toggle password visibility' })`
- `getByRole('button', { name: 'Forgot Password?' })`
- `getByRole('button', { name: 'Sign in with Google' })`
- `getByRole('button', { name: 'Sign in using SSO' })`
- `getByRole('button', { name: 'Sign in with Passkey' })`
- `getByRole('link', { name: 'Start a FREE TRIAL' })`
- `getByRole('link', { name: 'Privacy policy' })`
- `getByRole('link', { name: 'Terms' })`

### Execution and Reporting Rules

- Do not place real credentials in source control, test plans, screenshots, or logs.
- Mark a case `Blocked` when its credentials, expected behavior, browser matrix, or other required oracle is missing.
- Mark a case `Pass` only when its expected result is supported by supplied requirements or direct observation.
- Record URL, page title, visible response text, and console errors for each failed or blocked interaction.
- Repeat observed checks in a clean browser context to determine whether the result is reproducible.

## Self-Validation Check:

- The plan uses the supplied URL and only UI elements observed through Playwright MCP or explicitly described by the user.
- The empty-submit message is included because Playwright MCP observed it directly.
- No valid credentials, post-login page, API, error code, password policy, persistence rule, or browser matrix was invented.
- Unknown behavior is labeled as requiring an oracle, test data, or specification.
- Cases with missing requirements are not presented as pass criteria.
- The plan is deterministic only for the documented observation steps; backend-dependent outcomes remain `Insufficient information to determine.`