import { defineStore } from 'pinia'
import { plants as initialPlants } from '@/data/plants'
import {PLANT_CATEGORIES} from "@/data/plantCategories.js";

export const usePlantStore = defineStore('plants', {
    state: () => ({
        plants: initialPlants,
    }),

    getters: {
        bonsaiPlants: (state) =>
            state.plants.filter(p => p.category === PLANT_CATEGORIES.BONSAI),
        byCategory: (state, category) =>
            state.plants.filter(p => p.category === category),
    },

    actions: {
        find(id) {
            return this.plants.filter(p => p.id == id)
        },
        addPlant(plant) {
            this.plants.push(plant)
        },
    },
})