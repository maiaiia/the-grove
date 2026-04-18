<script setup>
import { useRouter } from 'vue-router'
import BrandLogo from '@/components/BrandLogo.vue'
import BrandDescription from '@/components/BrandDescription.vue'
import SplashActions from "@/components/splash-components/SplashActions.vue";
const router = useRouter()
</script>

<template>
  <div class="headline">
    <BrandLogo />
    <div class="headline__body">
      <BrandDescription />
      <SplashActions @enter="router.push('/grove')" @learn="router.push('#')" />
    </div>
  </div>
</template>

<style scoped>
.headline {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  box-sizing: border-box;
  height: 80vh;
  padding: 10px;
}

.headline__body {
  display: flex;
  flex-direction: column;
  gap: 32px;

  margin-top: auto;
}
</style>