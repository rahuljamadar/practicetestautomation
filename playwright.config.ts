import { defineConfig, devices } from '@playwright/test';

const isCI = Boolean(
  (globalThis as { process?: { env?: { CI?: string } } }).process?.env?.CI,
);

export default defineConfig({
  testDir: '.',
  testMatch: [
    '**/Basics_Playwright/**/*.spec.ts',
    '**/Basics_Playwright/**/*.test.ts',
    '**/katalon-demo-cura/tests/**/*.spec.ts',
    '**/katalon-demo-cura/tests/**/*.test.ts',
    '**/Practice_Web-Tables/tests/**/*.spec.ts',
    '**/Practice_Web-Tables/tests/**/*.test.ts',
  ],
  fullyParallel: true,
  forbidOnly: isCI,
  retries: isCI ? 2 : 0,
  workers: isCI ? 1 : undefined,
  reporter: [['html'], ['line'], ['allure-playwright']],
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
});
