import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json'
    }
})

export const plantApi = {
    async getAllPlants() {
        const response = await api.get('/api/plants/')
        return response.data
    },

    async getPlant(id) {
        const response = await api.get(`/api/plants/${id}`)
        return response.data
    },

}

export default api