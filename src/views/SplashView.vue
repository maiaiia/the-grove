<script setup>

import SplashNav from "@/components/SplashNav.vue";
import PlantShowcase from "@/components/PlantShowcase.vue";
import SplashHeadline from "@/components/SplashHeadline.vue";
import SplashStats from "@/components/SplashStats.vue";
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