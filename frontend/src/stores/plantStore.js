import { defineStore } from 'pinia'
import { plantApi } from '@/services/api'

export const usePlantStore = defineStore('plants', {
    state: () => ({
        plants: [],
        loading: false,
        error: null,
    }),

    getters: {
        byCategory: (state) => (category) =>
            state.plants.filter(p => p.category === category),

        allPlants: (state) => state.plants,
    },

    actions: {
        async fetchPlants() {
            this.loading = true
            try {
                const rawPlants = await plantApi.getAllPlants()
                this.plants = rawPlants.map(p => ({
                    ...p,
                    image: p.image ? `http://localhost:8000/${p.image.url}` : '/placeholder-plant.png'
                }))
            } catch (err) {
                this.error = err.message
            } finally {
                this.loading = false
            }
        },

        // Find plant by ID
        find(id) {
            return this.plants.find(p => p.id == id)
        },

        async addPlant(plant) {
            this.plants.push(plant)
            // TODO: await plantApi.createPlant(plant)
        },


        async updatePlant(updated) {
            const index = this.plants.findIndex(p => p.id === updated.id)
            if (index !== -1) {
                this.plants[index] = updated
                // TODO: await plantApi.updatePlant(updated.id, updated)
            }
        },


        async deletePlant(id) {
            this.plants = this.plants.filter(p => p.id !== id)
            // TODO: await plantApi.deletePlant(id)
        },
    },
})