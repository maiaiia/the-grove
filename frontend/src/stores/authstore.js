import { defineStore } from 'pinia'
import { authApi } from '@/services/gqlapi.js'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        loading: false,
        error: null,
    }),

    getters: {
        isAuthenticated: (state) => !!state.user,
        isAdmin: (state) => state.user?.role?.name === 'ADMIN',
        username: (state) => state.user?.username,
    },

    actions: {
        async login(username, password) {
            this.loading = true
            this.error = null
            try {
                const result = await authApi.login(username, password)
                this.user = result.user
                return result
            } catch (err) {
                this.error = err.message
                throw err
            } finally {
                this.loading = false
            }
        },

        async register(username, email, password) {
            this.loading = true
            this.error = null
            try {
                const user = await authApi.register(username, email, password)
                return user
            } catch (err) {
                this.error = err.message
                throw err
            } finally {
                this.loading = false
            }
        },

        async logout() {
            await authApi.logout()
            this.user = null
        },

        async checkAuth() {
            try {
                const result = await authApi.checkAuth()
                this.user = result.authenticated ? result.user : null
            } catch {
                this.user = null
            }
        }
    }
})