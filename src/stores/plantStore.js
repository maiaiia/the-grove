import { defineStore } from 'pinia'
import { plants as initialPlants } from '@/data/plants'

export const usePlantStore = defineStore('plants', {
    state: () => ({
        plants: initialPlants,
    }),

    getters: {
        byCategory: (state) => (category) =>
            state.plants.filter(p => p.category === category),
    },

    actions: {
        find(id) {
            return this.plants.filter(p => p.id == id)
        },
        addPlant(plant) {
            this.plants.push(plant)
        },
        updatePlant(updated) {
            const index = this.plants.findIndex(p => p.id === updated.id)
            if (index !== -1) this.plants[index] = updated
        },
        deletePlant(id){
            this.plants = this.plants.filter(p => p.id !== id)
        },
    },
})