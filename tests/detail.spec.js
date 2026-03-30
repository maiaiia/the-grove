import { test, expect } from '@playwright/test'

test.describe('Detail view', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/grove')
        await page.locator('.plant-card').first().click()
        await page.waitForURL(/\/plant\/\d+/)
    })

    test('shows plant name and latin name', async ({ page }) => {
        await expect(page.locator('.profile__name')).toBeVisible()
        await expect(page.locator('.profile__latin')).toBeVisible()
    })

    test('shows plant profile fields', async ({ page }) => {
        await expect(page.locator('.profile__section-label').first()).toContainText('Plant Profile')
        await expect(page.locator('.profile__field').first()).toBeVisible()
    })

    test('breadcrumb links back to grove', async ({ page }) => {
        await page.locator('.breadcrumb a').click()
        await expect(page).toHaveURL('/grove')
    })

    test('shows timeline section', async ({ page }) => {
        await expect(page.locator('.timeline__label')).toContainText('Growth Timeline')
    })
})