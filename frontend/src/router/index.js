import { createRouter, createWebHistory } from 'vue-router'
import SplashView     from '../views/SplashView.vue'
import MasterView      from '../views/MasterView.vue'
import DetailView     from '../views/DetailView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import RoadmapView    from '../views/RoadmapView.vue'
import SignInView from "@/views/SignInView.vue";
import RegisterView from "@/views/RegisterView.vue";
import ChatView from "@/views/ChatView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/',            component: SplashView },
        { path: '/grove',       component: MasterView },
        { path: '/plant/:id',   component: DetailView },
        { path: '/statistics',  component: StatisticsView },
        { path: '/roadmap',     component: RoadmapView },
        { path: '/sign-in',     component: SignInView },
        { path: '/register',    component: RegisterView },
        {path: '/chat',         component: ChatView},
    ]
})

export default router