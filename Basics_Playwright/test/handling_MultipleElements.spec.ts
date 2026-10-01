import { test, expect } from '@playwright/test';

test('Handling multiple elements', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/multiple_element_filter', {
        waitUntil: 'domcontentloaded',
        timeout: 60000,
    });

    const accountLinks = page.locator('a.list-group-item');
    const linkTexts = await accountLinks.allInnerTexts();

    expect(linkTexts).toHaveLength(13);
    console.log(linkTexts);

    const forgottenPasswordLink = accountLinks.filter({ hasText: 'Forgotten Password' });
    await expect(forgottenPasswordLink).toHaveCount(1);
    await forgottenPasswordLink.click();
    await expect(page).toHaveURL(/#forgotten-password$/);
});