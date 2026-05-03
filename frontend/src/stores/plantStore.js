import { defineStore } from 'pinia'
import {checkNetworkStatus, plantApi} from '@/services/gqlapi.js'

let PLANT_STORAGE       = 'grove_plants'
let SYNC_QUEUE_STORAGE  = 'grove_sync_queue'

let DELETE_OPERATION = 'DELETE'
let CREATE_OPERATION = 'CREATE'
let DELETE_PHOTO_OPERATION = 'DELETE_PHOTO'

let BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
                    photos: data.photos?.map(p => this._formatPhoto(p)) || [],
                    image: this._formatPhoto(data.image)
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
                this.totalPlants = data.totalPlants
            } catch (err) {
                this.error = "Could not load plant statistcs.";
                console.error(err);
            } finally {
                this.loading = false;
            }

        },

        async fetchPage(pageNumber, append = false) {
            // Skip if already loaded
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
                    image: p.image?.url
                        ? `${BASE_URL}/${p.image.url}`
                        : (typeof p.image === 'string' ? `${BASE_URL}/${p.image}` : '')
                }));

                this.totalPlants = response.total;

                if (append) {
                    this.plants.push(...mapped);
                } else {
                    this.plants = mapped;
                    this.loadedPages.clear();
                }

                this.loadedPages.add(pageNumber);
                this.saveToDisk();

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
        async handleNewPlantFromWebSocket(plantId) {
            try {
                const data = await plantApi.getPlant(plantId);
                const newPlant = {
                    ...data,
                    image: this._formatPhoto(data.image)
                };

                this.plants.push(newPlant);
                this.totalPlants++;

                const maxItems = this.loadedPages.size * this.pageSize + this.pageSize;
                if (this.plants.length > maxItems) {
                    this.plants = this.plants.slice(0, maxItems);
                }

                this.saveToDisk();

                await this.fetchPlantStatistics();

                console.log('[Store] New plant added via WebSocket:', newPlant.name);
            } catch (error) {
                console.error('[Store] Failed to fetch new plant:', error);
            }
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
                    image: response.image ? `${BASE_URL}/${response.image.url}` : ''
                };
                this.plants.push(newPlant);
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
            const originalPlants = [...this.plants];
            const originalTotal = this.totalPlants;

            this.plants = this.plants.filter(p => p.id !== id)
            this.totalPlants--;
            this.saveToDisk();

            const isOnline = await checkNetworkStatus();

            if (isOnline) {
                if (String(id).startsWith('temp')) return;
                try {
                    await plantApi.deletePlant(id)
                } catch (err) {
                    this.plants = originalPlants;
                    this.totalPlants = originalTotal;
                    this.saveToDisk();

                    this.error = "Permission denied or server error. Could not delete plant.";
                    throw err;
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

        async deletePhoto(photoId) {
            if (!this.currentPlant) return;

            const originalPhotos = [...this.currentPlant.photos];
            this.currentPlant.photos = this.currentPlant.photos.filter(p => p.id !== photoId);

            if (this.currentPlant.image?.id === photoId) {
                const nextPhoto = this.currentPlant.photos[this.currentPlant.photos.length - 1];
                this.currentPlant.image = nextPhoto || null;
            }

            const plantInList = this.plants.find(p => p.id === this.currentPlant.id);
            if (plantInList) {
                plantInList.image = this.currentPlant.image;
            }

            try {
                const isOnline = await checkNetworkStatus();
                if (isOnline) {
                    await plantApi.deletePhoto(photoId);
                    await this.fetchPlantStatistics();
                } else {
                    this.queueOperation({
                        type: DELETE_PHOTO_OPERATION,
                        photoId: photoId
                    });
                }
            } catch (err) {
                // Rollback on failure
                this.currentPlant.photos = originalPhotos;
                this.error = "Failed to delete photo.";
                console.error(err);
            }
        },
        async uploadPhoto(plantId, photoData) {
            try {
                const newPhoto = await plantApi.addPhoto(plantId, photoData);
                const formatted = this._formatPhoto(newPhoto);

                if (this.currentPlant && this.currentPlant.id === plantId) {
                    this.currentPlant.photos.push(formatted);
                    this.currentPlant.image = formatted;
                }

                const plantInList = this.plants.find(p => p.id === plantId);
                if (plantInList) {
                    plantInList.image = formatted;
                }

                return formatted;
            } catch (err) {
                this.error = "Failed to link photo.";
                console.error(err);
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
                            image: response.image ? `${BASE_URL}/${response.image.url}` : '',
                        };
                        this.saveToDisk();
                    }
                    break;
                }
                case DELETE_OPERATION: {
                    return await plantApi.deletePlant(operation.plantId);
                }
                case DELETE_PHOTO_OPERATION:{
                    return await plantApi.deletePhoto(operation.photoId);
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
        },
        _formatPhoto(photo) {
            if (!photo) return null;
            return {
                ...photo,
                url: photo.url.startsWith('http') ? photo.url : `${BASE_URL}/${photo.url}`
            };
        },
    },
})
