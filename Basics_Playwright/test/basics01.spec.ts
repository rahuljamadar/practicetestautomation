import { test, expect } from '@playwright/test'

test('test', async ({ page }) => {
    await page.goto("https://app.wingify.com/#/login");
    await expect(page).toHaveTitle("Wingify - Application")
});

test.skip('test2', async ({page})=> {
    
});

test.fail('test3', async ({page})=>{
   //this test is expected to fail 
});

test.only('test4', async ({page})=>{
    //this test will run exclusively
});

test.fixme('test5', async ({page})=>{
   //this test is expected to fix in future
});

test.slow('test6', async ({page})=>{
    //this test is expected to run slow
});