import { ref, onUnmounted } from "vue";
import api from "@/services/api.js";

const running = ref(false)
let webSocket = null

export function useSimulation(onPlantAdded) {

    function connect() {
        webSocket = new WebSocket('ws://localhost:8000/api/simulation/ws')

        webSocket.onopen = () => {
            console.log('[sim] websocket connected')
        }
        webSocket.onmessage = (e) => {
            console.log('[sim] message received:', e.data)
            const message = JSON.parse(e.data)
            if (message.event === 'plant_added') onPlantAdded(message.id)
        }
        webSocket.onerror = (e) => {
            console.error('[sim] websocket error:', e)
        }
        webSocket.onclose = () => {
            console.log('[sim] websocket closed')
            if (running.value) setTimeout(connect, 2000)
        }
    }

    async function start() {
        await api.post('/api/simulation/start')
        running.value = true
        connect()
    }

    async function stop() {
        await api.post('/api/simulation/stop')
        running.value = false
        webSocket?.close()
    }

    onUnmounted(() => webSocket?.close())

    return { running, start, stop }
}