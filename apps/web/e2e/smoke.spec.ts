
import { test, expect } from '@playwright/test';

test('landing page opens and can start trip planning', async ({ page }) => {
  await page.goto('/');

  // Verify landing page heading.
  await expect(
    page.getByRole('heading', {
      name: /your journey, thoughtfully planned/i,
    }),
  ).toBeVisible();

  // Navigate to trip planner.
  await page.getByRole('link', { name: /plan a trip/i }).first().click();

  // Verify trip planner heading.
  await expect(
    page.getByRole('heading', {
      name: /let’s plan your next journey/i,
    }),
  ).toBeVisible();
});
