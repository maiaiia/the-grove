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
    <PlantShowcase maxWidth="800px"/>
    <SplashStats />
  </div>
</template>

<style scoped>
.splash-view {
  display: flex;
  flex-direction: row;
  justify-content: space-between;

  padding: 5vh 5vw;
}
.stats{
  align-self: center;
}

.headline {
  justify-self: stretch;
}
</style>