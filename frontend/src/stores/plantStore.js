import { defineStore } from 'pinia'
import { plantApi } from '@/services/api'

export const usePlantStore = defineStore('plants', {
    state: () => ({
        plants: [],
        currentPlant: null,
        stats: [],
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

        async fetchPlantById(id) {
            this.loading = true;
            try {
                const data = await plantApi.getPlant(id);
                this.currentPlant = {
                    ...data,
                    photos: data.photos?.map(p => ({
                        ...p,
                        url: `http://localhost:8000/${p.url}`
                    })) || [],
                    image: data.image?.url
                        ? `http://localhost:8000/${data.image.url}`
                        : '/placeholder-plant.png'
                };
            } catch (err) {
                this.error = "Could not load plant details.";
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        async fetchPlantStatistics() {
            this.loading = true;
            try{
                const data = await plantApi.getStats();
                this.stats = data;
            } catch (err) {
                this.error = "Could not load plant statistcs.";
                console.error(err);
            } finally {
                this.loading = false;
            }

        },

        async addPlant(newPlantData) {
            try {
                const response = await plantApi.addPlant(newPlantData);
                this.plants.push({
                    ...response,
                    image: response.image ? `http://localhost:8000/${response.image.url}` : '/placeholder-plant.png'
                });
                await this.fetchPlantStatistics() //i don't really like this but i want stats to automatically refresh
            } catch (error) {
                console.error("Failed to plant the new friend:", error);
            }
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