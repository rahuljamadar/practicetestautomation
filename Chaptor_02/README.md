# Chaptor_02 Playwright Framework

This folder contains an industry-style Playwright test framework using Page Object Model (POM) and test planning for the login page at https://practicetestautomation.com/practice-test-login/.

## Structure
- `tests/` — test definitions
- `pages/` — page object classes
- `playwright.config.js` — Playwright configuration
- `TestPlan.md` — test plan and requirement mapping

## Notes
- Converted from TypeScript to JavaScript.
- Uses default XPath selectors only.
- Test credentials: Username `student`, Password `Password123`.

## How to Run
1. Open a terminal in `Chaptor_02`.
2. Install dependencies: `npm install`
3. Install Playwright browsers: `npx playwright install`
4. Run the tests: `npm test`
5. View the HTML report: `npm run test:report`

## Additional Information
- The tests use Playwright wait mechanisms instead of hard sleeps.
- The framework is designed for local execution; network access is required to download browsers.
