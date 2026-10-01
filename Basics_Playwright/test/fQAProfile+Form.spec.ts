import { test, expect } from '@playwright/test';

test('Verify profile submission', async ({ page }) => {

    await page.goto(
        'https://app.thetestingacademy.com/playwright/tables/practice#page',{
            waitUntil: 'domcontentloaded',
            timeout: 60000,
        }
    );

    await page.getByLabel('First Name').fill('Aarav');

    await page.getByLabel('Last Name').fill('Sharma');

    await page.getByTestId('gender-male').check();

    await page.getByTestId('years-experience').click();
    await page.getByLabel('Years of Experience').selectOption('5');

    await page.getByTestId('profile-date').fill('2023-01-01');

    await page.getByTestId('profession-manual').check();

    await page.locator('//*[text()=" Selenium Webdriver"]').click();

    await page.getByLabel('Asia').check();

    await page.getByRole('button', {
        name: 'Save profile'
    }).click();

    await expect(
        page.locator('.submission-output')
    ).toBeVisible();
});