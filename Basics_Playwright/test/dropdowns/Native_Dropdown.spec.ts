import { test, expect } from '@playwright/test';
test('Verify dropdown functionality', async ({ page }) => {
    await page.goto('https://the-internet.herokuapp.com/dropdown');
    await page.locator('#dropdown').click();
    await page.selectOption("#dropdown", "Option 2");
    //await expect(dropdown).toHaveValue('Java');

    await page.pause();
});