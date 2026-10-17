import { test, expect } from '@playwright/test';

test('Verify web table', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/multiple_element_filter');
    const innerTextLink: string[] = await page.locator('a.list-group-item').allInnerTexts();
    console.log(innerTextLink.length);

    for (const link of innerTextLink) {
        console.log(link);
    }

    for (const linkText of innerTextLink) {
        if (linkText === 'Forgotten Password') {
            await page.getByText(linkText).first().click();
        }
    }

    await page.pause();

});