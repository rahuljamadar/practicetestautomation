import { test, expect } from '@playwright/test';
test('Verify async dropdown', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/tables/select-boxes');
    await page.locator('#rs-async').click();
    await page.getByTestId('rs-async-input').fill('pun');

    await expect(page.getByTestId('rs-async-menu')).toContainText('Pune');
    await page.getByRole('option', { name: 'Pune', exact: true }).click();

    await page.pause();

});