import { test, expect } from '@playwright/test';
test('Verify custom dropdown', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/tables/dropdowns');
    await page.getByTestId('framework-trigger').click();
    await page.getByText('React').click();

    await page.pause();
});