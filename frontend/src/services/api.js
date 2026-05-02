import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ||'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json'
    }
})
export const checkNetworkStatus = async () => {
    if (!navigator.onLine) return false;

    try {
        await api.head('/api/health', { timeout: 3000 });
        return true;
    } catch {
        return false;
    }
}
export const plantApi = {
    async getAllPlants() {
        const response = await api.get('/api/plants/')
        return response.data
    },

    async getPlant(id) {
        const response = await api.get(`/api/plants/${id}`)
        return response.data
    },

    async getPage(pageNumber, plantsPerPage) {
        const response = await api.get(`/api/plants/page/${pageNumber}`, {
            params: { plants_per_page: plantsPerPage }
        });
        return response.data;
    },

    async getStats() {
        const response = await api.get('/api/stats')
        return response.data
    },

    async addPlant(plantData){
        const response = await api.post('/api/plants/', plantData)
        return response.data
    },

    async deletePlant(id){
        return await api.delete(`/api/plants/${id}`)
    },

    async updatePlant(updatedData){
        const {id, ...data} = updatedData
        const response = await api.put(`/api/plants/${id}`, data);
        return response.data;
    }
}

export default api