import { test, expect } from '@playwright/test';
test('Verify frames', async ({ page }) => {

    await page.goto('https://app.thetestingacademy.com/playwright/frames');

    let vehicleframe = await page.frameLocator('#frame-one');

    await vehicleframe.locator('RESULT_TextField-1').fill('Tata Nexon');

    await vehicleframe.locator('ownerName').fill('Rahul Jamadar');

    await vehicleframe.locator('regNumber').fill('MH12AB1234');

    await vehicleframe.locator('RESULT_RadioButton-1').selectOption('SUV');

    await vehicleframe.locator('RESULT_TextField-4').fill('2023');

    await vehicleframe.locator('notes').fill('This is a test note for the vehicle form');

    await vehicleframe.getByText('Submit registration').click();

    await page.pause();

});