import { describe, it, expect } from 'vitest'
import { createPlant } from '@/data/plants.js'
import { PLANT_CATEGORIES, PLANT_LOCATIONS } from '@/data/plantCategories.js'
const validData = {
    id: 1,
    name: 'Monstera Rex',
    latinName: 'Monstera deliciosa',
    category: PLANT_CATEGORIES.TROPICAL,
    datePlanted: '2023-01-01',
    wateringSchedule: 7,
    lastWatered: '2026-03-01',
    location: PLANT_LOCATIONS.INDOORS,
    photos: [],
    notes: '',
}

describe('createPlant', () => {
    it('creates a plant with correct fields', () => {
        const plant = createPlant(validData)
        expect(plant.id).toBe(1)
        expect(plant.name).toBe('Monstera Rex')
        expect(plant.latinName).toBe('Monstera deliciosa')
        expect(plant.category).toBe(PLANT_CATEGORIES.TROPICAL)
        expect(plant.location).toBe(PLANT_LOCATIONS.INDOORS)
        expect(plant.wateringSchedule).toBe(7)
        expect(plant.notes).toBe('')
        expect(plant.photos).toEqual([])
    })

    it('computes age correctly from datePlanted', () => {
        const plant = createPlant({ ...validData, datePlanted: '2020-01-01' })
        expect(plant.age).toBeGreaterThanOrEqual(5)
    })

    it('age is 0 for a plant planted today', () => {
        const today = new Date().toISOString().split('T')[0]
        const plant = createPlant({ ...validData, datePlanted: today })
        expect(plant.age).toBe(0)
    })

    it('returns null for latestPhoto when photos is empty', () => {
        const plant = createPlant({ ...validData, photos: [] })
        expect(plant.latestPhoto).toBeNull()
    })

    it('returns the most recent photo as latestPhoto', () => {
        const plant = createPlant({
            ...validData,
            photos: [
                { date: '2023-01-01', url: '/old.jpg', description: '' },
                { date: '2025-06-01', url: '/new.jpg', description: '' },
                { date: '2024-03-01', url: '/mid.jpg', description: '' },
            ]
        })
        expect(plant.latestPhoto.url).toBe('/new.jpg')
    })

    it('returns sortedPhotos in ascending date order', () => {
        const plant = createPlant({
            ...validData,
            photos: [
                { date: '2025-06-01', url: '/b.jpg', description: '' },
                { date: '2023-01-01', url: '/a.jpg', description: '' },
            ]
        })
        expect(plant.sortedPhotos[0].url).toBe('/a.jpg')
        expect(plant.sortedPhotos[1].url).toBe('/b.jpg')
    })

    it('defaults notes to empty string if not provided', () => {
        const plant = createPlant({ ...validData, notes: undefined })
        expect(plant.notes).toBe('')
    })

    it('defaults photos to empty array if not provided', () => {
        const plant = createPlant({ ...validData, photos: undefined })
        expect(plant.photos).toEqual([])
    })
})