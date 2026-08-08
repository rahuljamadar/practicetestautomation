import { expect } from '@playwright/test';
import { loginData } from '../data/loginData.js';

export class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = page.locator("xpath=//input[@name='username']");
    this.passwordInput = page.locator("xpath=//input[@name='password']");
    this.submitButton = page.locator("xpath=//button[text()='Submit']");
    this.errorMessage = page.locator("xpath=//div[@id='error']");
  }

  async goto() {
    await this.page.goto(loginData.loginUrl);
    await expect(this.page).toHaveURL(/practice-test-login/);
    await expect(this.usernameInput).toBeVisible();
  }

  async login(username, password) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectErrorMessage(expectedText) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toContainText(expectedText);
  }
}
