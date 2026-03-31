<script setup>
import HeroCard from "./HeroCard.vue"
import PlantCard from "./PlantCard.vue"
import { computed } from 'vue'

const props = defineProps({
  heroPlant: Object,
  gridPlants: Array
})

const hasMultipleCards = computed(() => props.gridPlants?.length > 1)
</script>

<template>
  <div class="visual-view-content">
    <HeroCard v-if="heroPlant" :plant="heroPlant" :key="heroPlant.id" class="hero-card" />
    <div class="grove__grid" :class="{ 'single-card': !hasMultipleCards }">
      <TransitionGroup name="grid-card" appear>
        <PlantCard
            v-for="(plant, index) in gridPlants"
            :key="plant.id"
            :plant="plant"
            :style="{ '--card-index': index }"
        />
      </TransitionGroup>
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

  transition: all 0.5s ease;
  transition-delay: 1s;
}

.grove__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 24px;
  min-height: 0;
}

.grid-card-enter-active {
  transition: all 0.5s ease;
  transition-delay: calc(var(--card-index) * 0.08s + 0.2s);
}

.grove__grid.single-card .grid-card-enter-active {
  transition-delay: 0.2s;
}

.grid-card-leave-active {
  transition: all 0.3s ease;
}

.grid-card-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

.grid-card-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.grid-card-move {
  transition: transform 0.4s ease;
}

@media (max-width: 768px) {
  .visual-view-content {
    grid-template-columns: 1fr;
  }
}
</style>