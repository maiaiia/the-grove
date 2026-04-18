import { test, expect } from '@playwright/test'

test.describe('Grove view', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/grove')
    })

    test('displays the eyebrow with plant count', async ({ page }) => {
        await expect(page.locator('.eyebrow__title')).toBeVisible()
        await expect(page.locator('.eyebrow__sub')).toContainText('plants')
    })

    test('displays hero card and plant grid', async ({ page }) => {
        await expect(page.locator('.hero-card')).toBeVisible()
        await expect(page.locator('.plant-card').first()).toBeVisible()
    })

    test('clicking a plant card navigates to detail view', async ({ page }) => {
        await page.locator('.plant-card').first().click()
        await expect(page).toHaveURL(/\/plant\/\d+/)
    })

    test('clicking hero card navigates to detail view', async ({ page }) => {
        await page.locator('.hero-card').click()
        await expect(page).toHaveURL(/\/plant\/\d+/)
    })

    test('pagination shows correct page buttons', async ({ page }) => {
        await expect(page.locator('.pagination__page').first()).toBeVisible()
    })

    test('clicking next page changes displayed plants', async ({ page }) => {
        const firstHeroName = await page.locator('.hero-card__name').textContent()
        const nextBtn = page.locator('.pagination__page').nth(1)
        if (await nextBtn.isVisible()) {
            await nextBtn.click()
            const newHeroName = await page.locator('.hero-card__name').textContent()
            expect(newHeroName).not.toBe(firstHeroName)
        }
    })
})