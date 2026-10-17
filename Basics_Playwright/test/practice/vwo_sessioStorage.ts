import { chromium } from 'playwright';
import dotenv from 'dotenv';

dotenv.config();

const username = process.env.VWO_USER;
const password = process.env.VWO_PASS;

async function saveSession() {
    let browser = await chromium.launch({ headless: false });
    let context = await browser.newContext();
    let page = await context.newPage();

    await page.goto("https://app.wingify.com/#/login");
    await page.locator('//input[@id="login-username"]').fill(username!);
    await page.locator('//input[@id="login-password"]').fill(password!);
    await page.locator('//button[@id="js-login-btn"]').click();

    await page.waitForURL(/#\/(dashboard|home)/, { timeout: 150000 });
    await page.waitForTimeout(3000);

    await context.storageState({ path: "./user-session.json" });
    console.log("Session save successfully");
    await browser.close();
}

saveSession();