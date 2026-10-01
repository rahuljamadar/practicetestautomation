import { test, expect } from '@playwright/test';

test('Verify web table', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/multiple_element_filter');
    const innerTextLinks: string[] = await page.locator('a.list-group-item').allInnerTexts();
    console.log(innerTextLinks.length);

    for (const links of innerTextLinks) {
        console.log(links);
    }

    for (const link of innerTextLinks) {
        if (link === 'Forgotten Password') {
            await page.getByText(link).first().click();
        }
    }

});