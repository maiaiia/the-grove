const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WS_URL = BASE_URL.replace('http', 'ws')

export const chatService = {
    async getHistory() {
        const res = await fetch(`${BASE_URL}/api/chat/history`, {
            credentials: 'include'
        })
        if (!res.ok) throw new Error('Failed to fetch history')
        return res.json()
    },

    connect(onMessage) {
        const token = sessionStorage.getItem('access_token')

        if (!token) {
            throw new Error('No authentication token found')
        }
        const ws = new WebSocket(`${WS_URL}/ws/chat?token=${encodeURIComponent(token)}`)
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)
            onMessage(data)
        }
        ws.onerror = (err) => console.error('WebSocket error:', err)
        return ws
    }
}