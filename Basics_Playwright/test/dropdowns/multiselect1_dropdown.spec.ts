import {test, expect} from '@playwright/test';
test('Verify multi select input dropdown', async ({page}) => {
await page.goto('https://app.thetestingacademy.com/playwright/tables/select-boxes');
await page.getByTestId('rs-creatable-input').click();
await page.getByText('api-testing', { exact: true }).click();
await page.getByText('accessibility',{exact: true}).click();
await page.getByText('visual-regression', {exact: true}).click();
await page.keyboard.press('Escape');

await page.pause();
});