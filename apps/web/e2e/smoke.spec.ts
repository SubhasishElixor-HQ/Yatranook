import { test, expect } from '@playwright/test';

test('landing page opens and can start trip planning', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('Your journey, thoughtfully planned.')).toBeVisible();
  await page.getByRole('link', { name: /plan a trip/i }).first().click();
  await expect(page.getByText('Let’s plan your next journey')).toBeVisible();
});
