import { chromium } from '@playwright/test';

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage();
  await page.goto('https://practicetestautomation.com/practice-test-login/');
  await page.fill("xpath=//input[@name='username']", 'student');
  await page.fill("xpath=//input[@name='password']", 'Password123');
  await page.click("xpath=//button[text()='Submit']");
  await page.waitForURL(/logged-in-successfully/);
  const content = await page.textContent("xpath=//h1 | //h2 | //p");
  console.log('login success page content:', content && content.trim().slice(0, 120));
  await browser.close();
})();
