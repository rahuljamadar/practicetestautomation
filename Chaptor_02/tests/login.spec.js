import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/loginPage.js';
import { loginData } from '../data/loginData.js';

test.describe('Practice Test Automation Login', () => {
  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('Positive login should navigate to success page', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login(loginData.validUsername, loginData.validPassword);
    await expect(page).toHaveURL(new RegExp(loginData.loggedInUrlPart));
    await expect(page.locator(loginData.successMessageLocator)).toBeVisible();
    await expect(page.locator(loginData.logoutButtonSelector)).toBeVisible();
  });

  test('Negative login with invalid username should show username error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login(loginData.invalidUsername, loginData.validPassword);
    await loginPage.expectErrorMessage(loginData.errorMessages.invalidUsername);
  });

  test('Negative login with invalid password should show password error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login(loginData.validUsername, loginData.invalidPassword);
    await loginPage.expectErrorMessage(loginData.errorMessages.invalidPassword);
  });

  test('Negative login with empty username should show username error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login('', loginData.validPassword);
    await loginPage.expectErrorMessage(loginData.errorMessages.invalidUsername);
  });

  test('Negative login with empty password should show password error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login(loginData.validUsername, '');
    await loginPage.expectErrorMessage(loginData.errorMessages.invalidPassword);
  });
});
