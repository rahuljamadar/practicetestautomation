import { test, expect } from '@playwright/test';

test('Verify login functionality', async ({ page }) => {

    await page.goto("https://app.wingify.com/#/login", {
        waitUntil: "domcontentloaded"
    });

    let username = page.getByRole("textbox", { name: "Email" });

    await username.fill("testuser@yopmail.com");

    let password = page.getByRole("textbox", { name: "password" });
    await password.fill("test123");

    let signInButton = page.getByRole("button", { name: "submit", exact: true });
    signInButton.click();
});