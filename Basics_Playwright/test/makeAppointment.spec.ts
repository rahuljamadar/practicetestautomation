import { test, expect } from '@playwright/test';

test('Make Appointment', async ({ page }) => {
    await page.goto('https://katalon-demo-cura.herokuapp.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 60_000,
    });

    await page.getByRole('link', { name: 'Make Appointment' }).click();

    // The page shows demo credentials in read-only textboxes with the same
    // accessible names, so target the actual login inputs by their IDs.
    await page.locator('#txt-username').fill('John Doe');
    await page.locator('#txt-password').fill('ThisIsNotAPassword');
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page.getByRole('heading', { name: 'Make Appointment' })).toBeVisible();
});