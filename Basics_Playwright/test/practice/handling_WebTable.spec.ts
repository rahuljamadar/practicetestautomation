import { test, expect } from '@playwright/test';

test('Handling web table', async ({ page }) => {
    await page.goto('https://app.thetestingacademy.com/playwright/webtable');

    const tableRows = page.locator('table[aria-label="Employee Management System table"] tbody tr');
    const rowCount = await tableRows.count();
    let targetFound = false;

    for (let i = 0; i < rowCount; i++) {
        const row = tableRows.nth(i);
        const username = (await row.locator('td').nth(1).innerText()).trim();

        if (username === 'Rohan.Mehta') {
            const checkbox = row.getByRole('checkbox');
            await checkbox.check();
            await expect(checkbox).toBeChecked();
            targetFound = true;
            break;
        }
    }

    expect(targetFound, 'Expected to find the Rohan.Mehta row').toBe(true);

    await page.pause();
});