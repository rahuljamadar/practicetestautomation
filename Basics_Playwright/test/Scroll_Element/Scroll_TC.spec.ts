import { test, expect } from '@playwright/test';

test.describe('Scroll to Element', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('https://app.thetestingacademy.com/playwright/widgets/scroll');

    });

    test('Scroll in to view', async ({ page }) => {
        await page.getByTestId('section-lazy').scrollIntoViewIfNeeded();
        await page.getByTestId('section-lazy').click();

        //using javascript evaluate function
        //await page.evaluate(()=> window.scrollBy(0, 100));

        //scroll to bottom
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

        //scroll to top
        // await page.evaluate(()=> window.scrollTo(0, 0));


        await page.pause();
    });


});