<template>
  <header class="navbar">
    <!-- Left: Logo -->
    <div class="logo">
      <img src="/logo-transparent.svg" width="46px" height="46px">
      <span class="brand"><router-link to= "/">The Grove</router-link></span>
    </div>

    <!-- Right: Navigation -->
    <nav class="nav-links">
      <router-link to="/chat" class="link">Chat</router-link>
      <router-link to="/statistics" class="link">Statistics</router-link>
      <router-link to="/grove" class="link">My Grove</router-link>

      <template v-if="authStore.isAuthenticated">
        <div class="divider" />
        <div class="user-cluster">
          <span class="username">{{ authStore.username }}</span>
          <button class="add-btn" @click="open">+ Add Plant</button>
          <button class="logout-btn" @click="handleLogout">↩</button>
        </div>
      </template>
      <router-link v-else to= "/sign-in" class="link">Log In</router-link>
    </nav>
  </header>
</template>

<script setup>
import { useAddPlantModal } from '@/composables/useAddPlantModal.js'
import { useRouter } from 'vue-router'
import {useAuthStore} from "@/stores/authstore.js";

const { open } = useAddPlantModal()
const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/sign-in')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 10px 48px;
  border-bottom: 1px solid var(--rodeo-dust);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon {
  display: flex;
  align-items: center;
  width: 46px;
  height: 46px;
}

.brand,
.brand a{
  color: var(--green-kelp);
  font-family: var(--playfair-display), "Playfair Display", serif;
  font-size: 18px;
  font-weight: 900;
  line-height: normal;
  letter-spacing: -0.5px;
}

.brand a{
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;

  font-family: 'Space Mono', monospace;
}

.link {
  text-decoration: none;
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--avocado);
  text-transform: uppercase;
}

.link:hover {
  color: #2f4f3f;
}

.add-btn {
  background: var(--green-kelp);
  color: var(--cream);
  text-align: center;
  border: none;
  padding: 8px 16px;
  text-transform: uppercase;
  cursor: pointer;

  font-family: 'Space Mono', monospace;
  font-size: 10px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1px;
}

.add-btn:hover {
  opacity: 0.9;
}
@media (max-width: 768px) {
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 10px 10px;
    border-bottom: 1px solid var(--rodeo-dust);
  }

  .logo {
    gap: 5px;
  }
  .nav-links {
    gap: 15px;
  }
  .link {
    font-size: 10px
  }
}

.username {
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--green-kelp);
  text-transform: uppercase;
  white-space: nowrap;
}

.logout-btn {
  background: transparent;
  border: 1px solid var(--rodeo-dust);
  color: var(--avocado);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  padding: 0;
}
.logout-btn:hover {
  border-color: var(--green-kelp);
  color: var(--green-kelp);
}
.divider {
  width: 1px;
  height: 20px;
  background-color: var(--rodeo-dust);
}
.user-cluster {
  display: flex;
  align-items: center;
  gap: 12px;
}

</style>