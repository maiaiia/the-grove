import { describe, it, expect } from 'vitest'

// same logic as in the modals
function validatePlantForm(form) {
    const errors = {}
    if (!form.name?.trim()) errors.name = 'Required'
    if (!form.latinName?.trim()) errors.latinName = 'Required'
    if (!form.category) errors.category = 'Required'
    if (!form.datePlanted) errors.datePlanted = 'Required'
    if (!form.wateringSchedule || form.wateringSchedule < 1)
        errors.wateringSchedule = 'Must be at least 1'
    if (!form.location) errors.location = 'Required'
    return errors
}

const validForm = {
    name: 'Monstera Rex',
    latinName: 'Monstera deliciosa',
    category: 'Tropical',
    datePlanted: '2023-01-01',
    wateringSchedule: 7,
    location: 'Indoors',
}

describe('validatePlantForm', () => {
    it('returns no errors for a valid form', () => {
        expect(validatePlantForm(validForm)).toEqual({})
    })

    it('requires name', () => {
        const errors = validatePlantForm({ ...validForm, name: '' })
        expect(errors.name).toBe('Required')
    })

    it('requires latinName', () => {
        const errors = validatePlantForm({ ...validForm, latinName: '' })
        expect(errors.latinName).toBe('Required')
    })

    it('requires category', () => {
        const errors = validatePlantForm({ ...validForm, category: '' })
        expect(errors.category).toBe('Required')
    })

    it('requires datePlanted', () => {
        const errors = validatePlantForm({ ...validForm, datePlanted: '' })
        expect(errors.datePlanted).toBe('Required')
    })

    it('requires wateringSchedule to be at least 1', () => {
        expect(validatePlantForm({ ...validForm, wateringSchedule: 0 }).wateringSchedule).toBeDefined()
        expect(validatePlantForm({ ...validForm, wateringSchedule: -1 }).wateringSchedule).toBeDefined()
        expect(validatePlantForm({ ...validForm, wateringSchedule: null }).wateringSchedule).toBeDefined()
    })

    it('accepts wateringSchedule of 1', () => {
        expect(validatePlantForm({ ...validForm, wateringSchedule: 1 }).wateringSchedule).toBeUndefined()
    })

    it('requires location', () => {
        const errors = validatePlantForm({ ...validForm, location: '' })
        expect(errors.location).toBe('Required')
    })

    it('catches multiple errors at once', () => {
        const errors = validatePlantForm({ name: '', latinName: '', category: '', datePlanted: '', wateringSchedule: 0, location: '' })
        expect(Object.keys(errors).length).toBe(6)
    })

    it('trims whitespace for name', () => {
        const errors = validatePlantForm({ ...validForm, name: '   ' })
        expect(errors.name).toBe('Required')
    })
})