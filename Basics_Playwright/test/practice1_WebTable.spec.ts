import { test, expect, Locator } from '@playwright/test';

test('Handling multiple elements1', async ({ page }) => {
    await page.goto("https://app.thetestingacademy.com/playwright/multiple_element_filter");

    const forgottenPasswordLink: Locator[] = await page.locator('a.list-group-item').all();
    console.log(forgottenPasswordLink.length);

    for (const link of forgottenPasswordLink) {
        console.log(await link.getAttribute('href'));
    }

    await page.pause();

});