<script setup>

import SplashNav from "@/components/splash-components/SplashNav.vue";
import PlantShowcase from "@/components/splash-components/PlantShowcase.vue";
import SplashHeadline from "@/components/splash-components/SplashHeadline.vue";
import SplashStats from "@/components/splash-components/SplashStats.vue";
</script>

<template>
    <SplashNav />
  <div class="splash-view">
    <SplashHeadline />
    <PlantShowcase />
    <SplashStats />
  </div>
</template>

<style scoped>
.splash-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 40px;

  padding: 80px 24px;
  width: 100%;
  min-height: 100vh;
  background-color: var(--parchment);
}

@media (min-width: 1024px) {
  .splash-view {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    height: 100vh;
    padding: 5vh 5vw;
    overflow: hidden;
  }
}

.stats {
  align-self: center;
}


.headline {
  width: 100%;
  text-align: center;
}

@media (min-width: 1024px) {
  .headline {
    width: auto;
    text-align: left;
  }
}
</style>