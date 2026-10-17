import { faker } from '@faker-js/faker';
import { test, expect } from '@playwright/test';

const testCases = [
    { description: 'valid-looking credentials', email: faker.internet.email(), password: faker.internet.password() },
    { description: 'random credentials', email: faker.internet.email(), password: faker.internet.password() },
    { description: 'empty username', email: '', password: faker.internet.password() },
    { description: 'empty password', email: faker.internet.email(), password: '' },
    { description: 'both empty', email: '', password: '' },
];

test.describe('Data Driven Testing with Faker', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('https://app.thetestingacademy.com/playwright/multiple_element_filter', {
            waitUntil: 'domcontentloaded',
        });
    });

    for (const data of testCases) {
        test(`submit form with ${data.description}`, async ({ page }) => {
            await page.locator('#email').fill(data.email);
            await page.locator('#password').fill(data.password);
            await page.getByTestId('login-button').click();
            await expect(page).toHaveURL(/#login-success$/);
        });
    }
});