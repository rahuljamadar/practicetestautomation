import { expect } from '@playwright/test';
import { loginData } from '../data/loginData.js';

export class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = page.locator('[name="username"]');
    this.passwordInput = page.locator('[name="password"]');
    this.submitButton = page.locator('button:has-text("Submit")');
    this.errorMessage = page.locator('#error');
    this.successMessage = page.locator(loginData.successMessageLocator);
    this.logoutButton = page.locator(loginData.logoutButtonSelector);
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

  async expectSuccessfulLogin() {
    await expect(this.page).toHaveURL(new RegExp(loginData.loggedInUrlPart));
    await expect(this.successMessage).toBeVisible();
    await expect(this.logoutButton).toBeVisible();
  }

  async expectErrorMessage(expectedText) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toContainText(expectedText);
  }
}
