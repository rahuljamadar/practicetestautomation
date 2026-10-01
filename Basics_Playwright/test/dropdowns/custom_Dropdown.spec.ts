import { test, expect } from '@playwright/test';
test('Verify custom dropdown', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/tables/dropdowns');
    await page.getByTestId('lang-trigger').click();
    await page.getByRole('option', { name: 'JavaScript' }).click();

    await page.pause();

});
