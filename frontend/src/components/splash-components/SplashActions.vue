<script setup>
import {useAuthStore} from "@/stores/authstore.js";
import {useRouter} from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const handleEnter = () => {
  if (authStore.isAuthenticated) {
    router.push('/grove');
  } else {
    router.push('/sign-in');
  }
};

const handleLearn = () => {
  router.push('/grove');
}

</script>

<template>
  <div class="splash-actions">
    <button class="btn btn--primary" @click="handleEnter">Enter the Grove</button>
    <button class="btn btn--outline" @click="handleLearn">Learn More</button>
  </div>
</template>

<style scoped>
.splash-actions {
  display: flex;
  gap: 12px;
}

.btn {
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 18px 32px;
  border: 1px solid transparent;
  cursor: pointer;
}

.btn--primary {
  background: var(--green-kelp);
  color: var(--parchment);
  border-color: var(--green-kelp);
}

.btn--outline {
  background: transparent;
  color: var(--avocado);
  border-color: var(--mongoose);
}

.btn--primary:hover { opacity: 0.85; }
.btn--outline:hover { border-color: var(--green-kelp); }
</style>