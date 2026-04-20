import { defineStore } from 'pinia'
import {checkNetworkStatus, plantApi} from '@/services/api'

let PLANT_STORAGE       = 'grove_plants'
let SYNC_QUEUE_STORAGE  = 'grove_sync_queue'

let DELETE_OPERATION = 'DELETE'

export const usePlantStore = defineStore('plants', {
    state: () => ({
        plants: [],
        currentPlant: null,
        stats: [],
        loading: false,
        error: null,

        syncQueue: [],
    }),

    getters: {
        byCategory: (state) => (category) =>
            state.plants.filter(p => p.category === category),

        allPlants: (state) => state.plants,
    },

    actions: {
        loadFromStorage() {
            this.plants = JSON.parse(localStorage.getItem(PLANT_STORAGE)) || [];
            this.syncQueue = JSON.parse(localStorage.getItem(SYNC_QUEUE_STORAGE)) || []
            console.log('Loaded data from the local storage')
        },
        saveToDisk() {
            localStorage.setItem(PLANT_STORAGE, JSON.stringify(this.plants));
            localStorage.setItem(SYNC_QUEUE_STORAGE, JSON.stringify(this.syncQueue))
        },
        generateTempId() {
            return `temp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        },
        queueOperation(operation) {
            this.syncQueue.push({
                ...operation,
                _timestamp: Date.now(),
                _operation_id: this.generateTempId()
            });
            this.saveToDisk();
            console.log(`Added operation ${operation.type} to sync queue`)
        },

        async fetchPlants() {
            if (!await checkNetworkStatus()) return;
            await this.syncWithServer();

            this.loading = true
            try {
                const rawPlants = await plantApi.getAllPlants()
                const mappedPlants = rawPlants.map(p => ({
                    ...p,
                    image: p.image ? `http://localhost:8000/${p.image.url}` : ''
                }))

                this.plants = mappedPlants;
                this.saveToDisk();
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
                        : ''
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
                    image: response.image ? `http://localhost:8000/${response.image.url}` : ''
                });
                await this.fetchPlantStatistics() //i don't really like this but i want stats to automatically refresh
            } catch (error) {
                console.error("Failed to plant the new friend:", error);
            }
        },

        async deletePlant(id) {
            this.plants = this.plants.filter(p => p.id !== id)
            this.saveToDisk();

            const isOnline = await checkNetworkStatus();

            if (isOnline) {
                try {
                    await plantApi.deletePlant(id)
                } catch (err) {
                    console.log("Failed to delete plant: ", err.message)
                }
            } else {
                this.queueOperation({
                    type: DELETE_OPERATION,
                    plant_id: id
                })
            }
        },

        async updatePlant(updated) {
            const index = this.plants.findIndex(p => p.id === updated.id)
            if (index !== -1) {
                this.plants[index] = updated
                await plantApi.updatePlant(updated)
                await this.fetchPlantById(updated.id)
            }
        },

        async syncWithServer() {
            if (this.syncQueue.length === 0 || !await checkNetworkStatus()) return;

            console.log(`Syncing ${this.syncQueue.length} operations`);

            const queueToProcess = [...this.syncQueue];

            for (const operation of queueToProcess) {
                try {
                    await this.processSyncOperation(operation);
                    this.syncQueue = this.syncQueue.filter(op => op._operation_id !== operation._operation_id);
                    this.saveToDisk();
                } catch (err) {
                    console.error(`Failed to sync operation ${operation.type} : ${operation._operation_id}:`, err.message)
                    break;
                }
            }

        },
        async processSyncOperation(operation) {
            switch (operation.type) {
                case DELETE_OPERATION: {
                    return await plantApi.deletePlant(operation.plant_id);
                }
                default:
                    console.warn("Unknown operation type:", operation.type);
                    return Promise.resolve();
            }
        },

        init() {
            this.loadFromStorage();

            /*
            setInterval(async () => {
                if (this.syncQueue.length > 0) {
                    const isOnline = await checkNetworkStatus();
                    if (isOnline) {
                        console.log("Heartbeat detected server. Auto-syncing queue...");
                        await this.syncWithServer();
                    }
                }
            }, 10000); */

            console.log("Plant Store Initialized");
        },
        clearSyncQueue() {
            this.syncQueue = [];
            this.saveToDisk();
            console.log('Cleared sync queue')
        }
    },
})
