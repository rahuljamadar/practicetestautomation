import { test, expect } from '@playwright/test';
test('Verify multi select dropdown', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/tables/select-boxes');
    await page.getByTestId('rs-multi').click();
    await page.getByText('JUnit').click();
    await page.getByText('Mocha', { exact: true }).click();
    await page.keyboard.press('Escape');


});