import { defineStore } from 'pinia'
import {chatService} from "@/services/chatService.js";

export const useChatStore = defineStore('chat', {
    state: () => ({
        messages: [],
        onlineUsers: [],
        connected: false,
        ws: null,
    }),

    actions: {
        async init() {
            this.messages = await chatService.getHistory()
            this.ws = chatService.connect((data) => {
                if (data.type === 'message') {
                    this.messages.push(data)
                    this.onlineUsers = data.onlineUsers || []
                } else if (data.type === 'system') {
                    this.messages.push(data)
                    this.onlineUsers = data.onlineUsers || []
                }
            })
            this.ws.onopen = () => { this.connected = true }
            this.ws.onclose = () => { this.connected = false }
        },

        send(text) {
            if (this.ws && this.connected) {
                this.ws.send(text)
            }
        },

        disconnect() {
            if (this.ws) {
                this.ws.close()
                this.ws = null
            }
        }
    }
})