import { defineStore } from 'pinia'
import {checkNetworkStatus, plantApi} from '@/services/api'

let PLANT_STORAGE       = 'grove_plants'
let SYNC_QUEUE_STORAGE  = 'grove_sync_queue'

let DELETE_OPERATION = 'DELETE'
let CREATE_OPERATION = 'CREATE'

export const usePlantStore = defineStore('plants', {
    state: () => ({
        plants: [],
        currentPlant: null,
        stats: [],
        loading: false,
        error: null,

        totalPlants: 0,
        pageSize: 20,
        loadedPages: new Set(),

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

        async fetchPage(pageNumber, append = false) {
            // Skip if already loaded (for infinite scroll)
            if (this.loadedPages.has(pageNumber)) {
                console.log(`Page ${pageNumber} already loaded, skipping fetch`)
                return true
            }

            if (!await checkNetworkStatus()) {
                console.log('Offline - using cached data')
                return false
            }

            await this.syncWithServer();

            this.loading = true;
            try {
                const response = await plantApi.getPage(pageNumber, this.pageSize);
                const mapped = response.plants.map(p => ({
                    ...p,
                    image: p.image ? `http://localhost:8000/${p.image.url}` : ''
                }));

                this.totalPlants = response.total;

                if (append) {
                    // Append for infinite scroll
                    this.plants.push(...mapped);
                } else {
                    // Replace for initial load or view switch
                    this.plants = mapped;
                    this.loadedPages.clear(); // Reset loaded pages
                }

                this.loadedPages.add(pageNumber);
                this.saveToDisk();

                // Return whether there's more data
                return mapped.length > 0;
            } catch (err) {
                this.error = err.message;
                return false;
            } finally {
                this.loading = false;
            }
        },
        resetPages() {
            this.plants = [];
            this.loadedPages.clear();
        },
        async addPlant(newPlantData) {
            const isOnline = await checkNetworkStatus();
            if (!isOnline) {
                return this.handleOfflineAdd(newPlantData);
            }

            try {
                const response = await plantApi.addPlant(newPlantData);
                const newPlant = {
                    ...response,
                    image: response.image ? `http://localhost:8000/${response.image.url}` : ''
                };
                this.plants.unshift(newPlant);
                this.totalPlants++;
                this.saveToDisk();
                await this.fetchPlantStatistics();

                return newPlant;
            } catch (error) {
                console.error("Failed to add plant:", error);
                throw error;
            }
        },
        handleOfflineAdd(plantData) {
            const tempId = this.generateTempId();
            const tempPlant = {
                ...plantData,
                id: tempId,
            };

            this.plants.unshift(tempPlant);
            this.queueOperation({
                type: CREATE_OPERATION,
                data: plantData,
                tempId: tempId
            })
            this.saveToDisk();

            console.log('Plant queued for sync:', tempPlant);
            return tempPlant;
        },

        async deletePlant(id) {
            this.plants = this.plants.filter(p => p.id !== id)
            this.saveToDisk();

            const isOnline = await checkNetworkStatus();

            if (isOnline) {
                if (String(id).startsWith('temp')) return;
                try {
                    await plantApi.deletePlant(id)
                } catch (err) {
                    console.log("Failed to delete plant: ", err.message)
                }
            } else {
                if (String(id).startsWith('temp_')) {
                    this.syncQueue = this.syncQueue.filter(
                        op => !(op.type === CREATE_OPERATION && op.tempId === id)
                    );
                    this.saveToDisk();
                }
                else {
                    this.queueOperation({
                        type: DELETE_OPERATION,
                        plantId: id
                    })
                }
            }
        },

        async updatePlant(updated) {
            const index = this.plants.findIndex(p => p.id === updated.id)
            if (index === -1) return;
            try {
                this.plants[index] = updated
                await plantApi.updatePlant(updated)
                await this.fetchPlantById(updated.id)
            } catch (e) {
                this.error = "Could not update plant details.";
                console.error(e);
                throw e;
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
                case CREATE_OPERATION: {
                    const response = await plantApi.addPlant(operation.data);
                    const index = this.plants.findIndex(p => p.id === operation.tempId)
                    if (index !== -1) {
                        this.plants[index] = {
                            ...response,
                            image: response.image ? `http://localhost:8000/${response.image.url}` : '',
                        };
                        this.saveToDisk();
                    }
                    break;
                }
                case DELETE_OPERATION: {
                    return await plantApi.deletePlant(operation.plantId);
                }
                default:
                    console.warn("Unknown operation type:", operation.type);
                    return Promise.resolve();
            }
        },

        init() {
            //this.clearSyncQueue();
            this.loadFromStorage();

            console.log("Plant Store Initialized");
        },
        clearSyncQueue() {
            this.syncQueue = [];
            this.saveToDisk();
            console.log('Cleared sync queue')
        }
    },
})
