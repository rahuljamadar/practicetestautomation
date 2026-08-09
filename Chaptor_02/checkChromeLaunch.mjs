import { chromium } from '@playwright/test';

(async () => {
  try {
    const browser = await chromium.launch({ channel: 'chrome', headless: true });
    console.log('Launched Chrome with version:', await browser.version());
    await browser.close();
    process.exit(0);
  } catch (error) {
    console.error('Browser launch failed:', error);
    process.exit(1);
  }
})();
