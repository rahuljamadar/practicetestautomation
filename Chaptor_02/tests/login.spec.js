import { test } from '@playwright/test';
import { LoginPage } from '../pages/loginPage.js';
import { loginData } from '../data/loginData.js';

const negativeCases = [
  {
    title: 'invalid username',
    username: loginData.invalidUsername,
    password: loginData.validPassword,
    expectedError: loginData.errorMessages.invalidUsername,
  },
  {
    title: 'invalid password',
    username: loginData.validUsername,
    password: loginData.invalidPassword,
    expectedError: loginData.errorMessages.invalidPassword,
  },
  {
    title: 'empty username',
    username: '',
    password: loginData.validPassword,
    expectedError: loginData.errorMessages.invalidUsername,
  },
  {
    title: 'empty password',
    username: loginData.validUsername,
    password: '',
    expectedError: loginData.errorMessages.invalidPassword,
  },
];

test.describe('Practice Test Automation Login', () => {
  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('Positive login should navigate to success page', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login(loginData.validUsername, loginData.validPassword);
    await loginPage.expectSuccessfulLogin();
  });

  for (const caseData of negativeCases) {
    test(`Negative login with ${caseData.title} should show error`, async ({ page }) => {
      const loginPage = new LoginPage(page);
      await loginPage.login(caseData.username, caseData.password);
      await loginPage.expectErrorMessage(caseData.expectedError);
    });
  }
});
