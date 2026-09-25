import { test, expect } from '@playwright/test';

test.use(
    {
        storageState: './user-session.json'

    });

test.setTimeout(60000);

test("Verify dashboard1- no login", async ({ page }) => {
    await page.goto("https://app.wingify.com/#/dashboard", { waitUntil: 'domcontentloaded', timeout: 60000 });
    await expect(page).toHaveURL(/dashboard/);
    console.log("Dashboard page is opened successfully without login");

});

test("Verify dashboard2- no login", async ({ page }) => {
    await page.goto("https://app.wingify.com/#/dashboard", { waitUntil: 'domcontentloaded', timeout: 60000 });
    await expect(page).toHaveURL(/dashboard/);
    console.log("Dashboard page is opened successfully without login");

});

test("Verify dashboard3- no login", async ({ page }) => {
    await page.goto("https://app.wingify.com/#/dashboard", { waitUntil: 'domcontentloaded', timeout: 60000 });
    await expect(page).toHaveURL(/dashboard/);
    console.log("Dashboard page is opened successfully without login");

});

test("Verify dashboard4- no login", async ({ page }) => {
    await page.goto("https://app.wingify.com/#/dashboard", { waitUntil: 'domcontentloaded', timeout: 60000 });
    await expect(page).toHaveURL(/dashboard/);
    console.log("Dashboard page is opened successfully without login");

});

test("Verify dashboard5- no login", async ({ page }) => {
    await page.goto("https://app.wingify.com/#/dashboard", { waitUntil: 'domcontentloaded', timeout: 60000 });
    await expect(page).toHaveURL(/dashboard/);
    console.log("Dashboard page is opened successfully without login");

});
