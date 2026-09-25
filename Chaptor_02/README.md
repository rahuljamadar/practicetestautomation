# Chapter 02 Playwright Framework

A clean Playwright test framework for the login page at https://practicetestautomation.com/practice-test-login/.

## Project structure
- `tests/` — test definitions
- `pages/` — page objects
- `data/` — reusable test data and locators
- `playwright.config.js` — framework configuration
- `playwright-report/` — generated reports

## Improvements
- Page Object Model implemented for login page behavior
- Reusable test data in a separate module
- Explicit success and error assertions
- Browser matrix with Chromium and Firefox
- CI-friendly retry and worker configuration
- HTML report generation on test runs

## Run locally
```bash
cd Chaptor_02
npm install
npx playwright install
npm test
```

## View report
```bash
npm run test:report
```

## Notes
- Use `BASE_URL` to target environments other than production.
- The framework uses Playwright's built-in locators, waits, and trace support.
