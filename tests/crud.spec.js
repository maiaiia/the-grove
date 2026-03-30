import { test, expect } from '@playwright/test'

test.describe('Add plant', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/grove')
    })

    test('opens add plant modal from nav button', async ({ page }) => {
        await page.locator('button', { hasText: '+ Add Plant' }).click()
        await expect(page.locator('.modal')).toBeVisible()
        await expect(page.locator('.modal__eyebrow')).toContainText('Add to your collection')
    })

    test('shows validation errors on empty submit', async ({ page }) => {
        await page.locator('button', { hasText: '+ Add Plant' }).click()
        await page.locator('button', { hasText: 'Add to Grove' }).click()
        await expect(page.locator('.modal__error').first()).toBeVisible()
    })

    test('closes modal on backdrop click', async ({ page }) => {
        await page.locator('button', { hasText: '+ Add Plant' }).click()
        await expect(page.locator('.modal')).toBeVisible()
        await page.locator('.modal-backdrop').click({ position: { x: 10, y: 10 } })
        await expect(page.locator('.modal')).not.toBeVisible()
    })

    test('successfully adds a new plant', async ({ page }) => {
        const countBefore = await page.locator('.eyebrow__sub').textContent()

        await page.locator('button', { hasText: '+ Add Plant' }).click()
        await page.locator('input[placeholder="e.g. Monstera Rex"]').fill('Test Fern')
        await page.locator('input[placeholder="e.g. Monstera deliciosa"]').fill('Pteridium aquilinum')
        await page.locator('select').nth(0).selectOption({ index: 1 })
        await page.locator('select').nth(1).selectOption({ index: 1 })
        await page.locator('input[type="date"]').fill('2022-06-15')
        await page.locator('input[type="number"]').fill('5')
        await page.locator('button', { hasText: 'Add to Grove' }).click()

        await expect(page.locator('.modal')).not.toBeVisible()
        const countAfter = await page.locator('.eyebrow__sub').textContent()
        expect(countAfter).not.toBe(countBefore)
    })
})

test.describe('Edit plant', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/grove')
        await page.locator('.plant-card').first().click()
        await page.waitForURL(/\/plant\/\d+/)
    })

    test('opens edit modal from detail view', async ({ page }) => {
        await page.locator('button', { hasText: 'Edit Plant Details' }).click()
        await expect(page.locator('.modal')).toBeVisible()
    })

    test('edit modal is pre-filled with plant data', async ({ page }) => {
        await page.locator('button', { hasText: 'Edit Plant Details' }).click()
        const nameInput = page.locator('input').first()
        const value = await nameInput.inputValue()
        expect(value.length).toBeGreaterThan(0)
    })

    test('can update plant name', async ({ page }) => {
        await page.locator('button', { hasText: 'Edit Plant Details' }).click()
        await page.locator('input').first().fill('Updated Plant Name')
        await page.locator('button', { hasText: 'Save Changes' }).click()
        await expect(page.locator('.modal')).not.toBeVisible()
        await expect(page.locator('.profile__name')).toContainText('Updated Plant Name')
    })
})

test.describe('Delete plant', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/grove')
        await page.locator('.plant-card').first().click()
        await page.waitForURL(/\/plant\/\d+/)
    })

    test('opens delete confirmation modal', async ({ page }) => {
        await page.locator('button', { hasText: 'Remove from Grove' }).click()
        await expect(page.locator('.modal')).toBeVisible()
        await expect(page.locator('.modal__eyebrow')).toContainText('cannot be undone')
    })

    test('cancelling delete keeps the plant', async ({ page }) => {
        const url = page.url()
        await page.locator('button', { hasText: 'Remove from Grove' }).click()
        await page.locator('button', { hasText: 'Keep it' }).click()
        await expect(page.locator('.modal')).not.toBeVisible()
        expect(page.url()).toBe(url)
    })

    test('confirming delete redirects to grove', async ({ page }) => {
        await page.locator('button', { hasText: 'Remove from Grove' }).click()
        await page.locator('button', { hasText: 'Yes, remove it' }).click()
        await expect(page).toHaveURL('/grove')
    })
})