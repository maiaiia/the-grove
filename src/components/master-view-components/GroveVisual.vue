<script setup>
import HeroCard from "./HeroCard.vue"
import PlantCard from "./PlantCard.vue"

const props = defineProps({
  heroPlant: Object,
  gridPlants: Array
})
</script>

<template>
  <div class="visual-view-content">
    <HeroCard v-if="heroPlant" :plant="heroPlant" class="hero-card" />
    <div class="grove__grid">
      <PlantCard v-for="plant in gridPlants" :key="plant.id" :plant="plant" />
    </div>
  </div>
</template>

<style scoped>
.visual-view-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  min-height: 0;
}

.hero-card {
  height: 100%;
  aspect-ratio: unset;
}

.grove__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 24px;
  min-height: 0;
}
</style>