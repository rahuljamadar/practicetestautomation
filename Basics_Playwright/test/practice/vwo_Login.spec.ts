import { test, expect } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

const username= process.env.VWO_USER;
const password= process.env.VWO_PASS;

test('Verify login functionality', async ({ page }) => {

    await page.goto("https://app.wingify.com/#/login");
    await page.locator('//input[@id="login-username"]').fill("VWO_USER");
    await page.locator('//input[@id="login-password"]').fill("VWO_PASS");
    await page.locator('//button[@id="js-login-btn"]').click();

    let expectedError = "Your email, password, IP address or location did not match";
    let errorMessage = page.locator('//div[text()="Your email, password, IP address or location did not match"]');

    await expect(errorMessage).toHaveText(expectedError);

    await page.pause();

});