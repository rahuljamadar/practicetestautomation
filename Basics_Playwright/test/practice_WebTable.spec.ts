import { test, expect } from '@playwright/test';

test('Handling multiple elements1', async ({ page }) => {
    await page.goto("https://app.thetestingacademy.com/playwright/multiple_element_filter");

    const forgottenPasswordLink: string[] = await page.locator('a.list-group-item').allInnerTexts();
    console.log(forgottenPasswordLink.length);

    await page.pause

});