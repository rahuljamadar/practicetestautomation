import { test, expect } from '@playwright/test';
test.describe('Scroll to element', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('https://app.thetestingacademy.com/playwright/widgets/scroll');

    });

    test('Scroll to element', async ({ page }) => {
        await page.getByTestId('cta-button').scrollIntoViewIfNeeded();
        await page.getByTestId('cta-button').click();

        expect(page.getByTestId('cta-button')).toBeVisible();

        await page.pause();

    });

});