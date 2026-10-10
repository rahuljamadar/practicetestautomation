# Wingify Login Test Execution Results

Source: [Wingify_Login_TestCases.md](Wingify_Login_TestCases.md)

Execution date: `2026-09-20`

Execution tool: Playwright MCP

Target: `https://app.wingify.com/#/login`

## Summary

- Executed: 20 listed test cases, to the extent supported by the supplied data and observable UI.
- Observed pass: 10 cases.
- Blocked or partially executable: 10 cases.
- No valid account credentials were used.
- The application reported console errors and warnings during the run; their meaning was not determined.

## Positive Results

| Case | Result | Evidence |
|---|---|---|
| WLG-POS-001 | Pass | Page loaded at the target URL with title `Login - Wingify`; required login controls and supporting links were present in the Playwright snapshot. |
| WLG-POS-002 | Pass | `test@example.com` was entered into `Email address`; the page remained on the login URL. |
| WLG-POS-003 | Pass | `Secret123!` was entered into `Password`; the page remained on the login URL. |
| WLG-POS-004 | Partial | `Toggle password visibility` was selected successfully. The exact masked/visible state transition was not observable in the resulting snapshot. |
| WLG-POS-005 | Blocked | Valid credentials and expected post-login URL, title, and landing-page criteria were not supplied. |
| WLG-POS-006 | Blocked | Valid credentials and Remember-me persistence requirements were not supplied. |
| WLG-POS-007 | Pass | Selecting `Forgot Password?` changed the route to `https://app.wingify.com/#/forgot-password`; the page displayed an email field, `Back`, and `Reset Password`. |
| WLG-POS-008 | Partial | Google opened a Google Accounts sign-in tab. SSO changed the route to `https://app.wingify.com/#/sso`. Passkey remained on the login route after selection. End-to-end authentication outcomes were not tested. |
| WLG-POS-009 | Pass | Trial, Privacy policy, and Terms each opened an external tab. The observed destinations were the Wingify/VWO pages represented by their link URLs. |
| WLG-POS-010 | Partial | Four keyboard `Tab` presses were executed; focus reached the `Start a FREE TRIAL` link. Full focus-order and accessibility acceptance criteria were not supplied. |

## Negative Results

| Case | Result | Evidence |
|---|---|---|
| WLG-NEG-001 | Pass | In a newly opened browser page with both fields empty, selecting `Sign in` displayed `Your email, password, IP address or location did not match` and stayed on the login route. |
| WLG-NEG-002 | Partial | A non-approved sample credential flow was not used as an account-validity assertion. The application response was observed during invalid-input runs, but approved invalid credentials and an error oracle were not supplied. |
| WLG-NEG-003 | Pass for observed response | With an empty email and `Secret123!` in the password field, selecting `Sign in` displayed `Your email, password, IP address or location did not match`. |
| WLG-NEG-004 | Pass for observed response | With `test@example.com` and an empty password, selecting `Sign in` displayed `Your email, password, IP address or location did not match`. |
| WLG-NEG-005 | Pass for observed response | With `not-an-email` and `Secret123!`, selecting `Sign in` displayed `Your email, password, IP address or location did not match`. No separate client-side format message was observed. |
| WLG-NEG-006 | Pass | The empty email and empty password submission was repeated after closing and reopening the Playwright page; the observed response was displayed again. |
| WLG-NEG-007 | Blocked | Password policy was not supplied. |
| WLG-NEG-008 | Blocked | Interruption requirements for Google, SSO, and Passkey flows were not supplied; no authentication cancellation was performed. |
| WLG-NEG-009 | Blocked | Remember-me persistence requirements and valid credentials were not supplied. |
| WLG-NEG-010 | Blocked | No approved viewport or responsive acceptance criteria were supplied. |

## Observed Routes and Links

- Login route: `https://app.wingify.com/#/login`
- Forgot-password route: `https://app.wingify.com/#/forgot-password`
- SSO route: `https://app.wingify.com/#/sso`
- Google authentication opened a Google Accounts sign-in URL in a new tab.
- The trial link opened a Wingify free-trial page in a new tab.
- The Privacy policy link opened a Wingify privacy-policy page in a new tab.
- The Terms link opened a Wingify terms page in a new tab.

## Limitations

- `test@example.com`, `Secret123!`, and `not-an-email` were used only as non-production input samples, not as claims about account validity.
- The observed message is reported exactly as rendered; its server-side meaning was not inferred.
- Console errors and warnings were observed but not diagnosed because no diagnostic requirement or source access was provided.
- A successful-login result cannot be determined without approved credentials and post-login acceptance criteria.