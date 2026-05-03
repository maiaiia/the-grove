import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import {createPinia} from "pinia";
import {useAuthStore} from "@/stores/authstore.js";


const app = createApp(App)
app.use(router)
app.use(createPinia())

const authStore = useAuthStore();
authStore.checkAuth().finally(() => {
    app.mount('#app')
})