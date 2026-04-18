import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { usePlantStore } from '@/stores/plantStore.js'
import { createPlant } from '@/data/plants.js'
import { PLANT_CATEGORIES, PLANT_LOCATIONS } from '@/data/plantCategories.js'


const makePlant = (overrides = {}) => createPlant({
    id: 99,
    name: 'Test Plant',
    latinName: 'Testus plantus',
    category: PLANT_CATEGORIES.TROPICAL,
    datePlanted: '2022-01-01',
    wateringSchedule: 7,
    lastWatered: '2026-03-01',
    location: PLANT_LOCATIONS.INDOORS,
    photos: [],
    notes: '',
    ...overrides,
})

describe('plantStore', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
    })

    // READ
    describe('initial state', () => {
        it('loads initial plants from data file', () => {
            const store = usePlantStore()
            expect(store.plants.length).toBeGreaterThan(0)
        })

        it('byCategory returns only plants of the given category', () => {
            const store = usePlantStore()
            const bonsai = store.byCategory(PLANT_CATEGORIES.BONSAI)
            expect(bonsai.every(p => p.category === PLANT_CATEGORIES.BONSAI)).toBe(true)
        })
        it('byCategory returns empty array for unknown category', () => {
            const store = usePlantStore()
            expect(store.byCategory('unknown')).toEqual([])
        })
    })

    // CREATE
    describe('addPlant', () => {
        it('adds a plant to the list', () => {
            const store = usePlantStore()
            const before = store.plants.length
            store.addPlant(makePlant())
            expect(store.plants.length).toBe(before + 1)
        })

        it('added plant has correct data', () => {
            const store = usePlantStore()
            store.addPlant(makePlant({ id: 99, name: 'Test Plant' }))
            const found = store.plants.find(p => p.id === 99)
            expect(found).toBeDefined()
            expect(found.name).toBe('Test Plant')
        })

        it('can add multiple plants', () => {
            const store = usePlantStore()
            const before = store.plants.length
            store.addPlant(makePlant({ id: 101 }))
            store.addPlant(makePlant({ id: 102 }))
            expect(store.plants.length).toBe(before + 2)
        })
    })

    // UPDATE
    describe('updatePlant', () => {
        it('updates an existing plant', () => {
            const store = usePlantStore()
            store.addPlant(makePlant({ id: 99, name: 'Old Name' }))
            store.updatePlant(makePlant({ id: 99, name: 'New Name' }))
            const found = store.plants.find(p => p.id === 99)
            expect(found.name).toBe('New Name')
        })

        it('does not change plant count when updating', () => {
            const store = usePlantStore()
            store.addPlant(makePlant({ id: 99 }))
            const before = store.plants.length
            store.updatePlant(makePlant({ id: 99, name: 'Updated' }))
            expect(store.plants.length).toBe(before)
        })

        it('does nothing if plant id does not exist', () => {
            const store = usePlantStore()
            const before = store.plants.length
            store.updatePlant(makePlant({ id: 9999, name: 'Ghost' }))
            expect(store.plants.length).toBe(before)
            expect(store.plants.find(p => p.id === 9999)).toBeUndefined()
        })

        it('updates only the target plant', () => {
            const store = usePlantStore()
            store.addPlant(makePlant({ id: 99, name: 'Plant A' }))
            store.addPlant(makePlant({ id: 100, name: 'Plant B' }))
            store.updatePlant(makePlant({ id: 99, name: 'Plant A Updated' }))
            expect(store.plants.find(p => p.id === 100).name).toBe('Plant B')
        })
    })

    // DELETE
    describe('deletePlant', () => {
        it('removes a plant by id', () => {
            const store = usePlantStore()
            store.addPlant(makePlant({ id: 99 }))
            store.deletePlant(99)
            expect(store.plants.find(p => p.id === 99)).toBeUndefined()
        })

        it('reduces plant count by 1', () => {
            const store = usePlantStore()
            store.addPlant(makePlant({ id: 12345 }))
            const before = store.plants.length
            store.deletePlant(12345)
            expect(store.plants.length).toBe(before - 1)
        })

        it('does nothing if id does not exist', () => {
            const store = usePlantStore()
            const before = store.plants.length
            store.deletePlant(9999)
            expect(store.plants.length).toBe(before)
        })

        it('does not remove other plants', () => {
            const store = usePlantStore()
            store.addPlant(makePlant({ id: 99 }))
            store.addPlant(makePlant({ id: 100 }))
            store.deletePlant(99)
            expect(store.plants.find(p => p.id === 100)).toBeDefined()
        })
    })
})