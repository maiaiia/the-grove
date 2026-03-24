<script setup>
import AppNav from "@/components/AppNav.vue"
import GroveEyebrow from "@/components/master-view-components/GroveEyebrow.vue"
import HeroCard from "@/components/master-view-components/HeroCard.vue"
import PlantCard from "@/components/master-view-components/PlantCard.vue"
import GrovePagination from "@/components/master-view-components/GrovePagination.vue"
import { computed, ref } from 'vue'
import { usePlantStore } from '@/stores/plantStore'

const store = usePlantStore()
const currentPage = ref(1)
const perPage = 5 // 1 hero + 4 small

const totalPages = computed(() => Math.ceil(store.plants.length / perPage))

const heroPlant = computed(() => store.plants[(currentPage.value - 1) * perPage])
const gridPlants = computed(() => store.plants.slice(
    (currentPage.value - 1) * perPage + 1,
    currentPage.value * perPage
))
</script>

<template>
  <div class="grove">
    <AppNav class="grove__nav" />
    <div class="grove__inner">
      <GroveEyebrow :count="store.plants.length" />
      <div class="grove__content">
        <HeroCard v-if="heroPlant" :plant="heroPlant" />
        <div class="grove__grid">
          <PlantCard v-for="plant in gridPlants" :key="plant.id" :plant="plant" />
        </div>
      </div>
      <GrovePagination :current="currentPage" :total="totalPages" @change="currentPage = $event" />
    </div>
  </div>
</template>

<style scoped>
.grove {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.grove__inner {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 24px 48px;
  gap: 20px;
  min-height: 0;
}

.grove__content {
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
.plant-card__image-wrapper {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  aspect-ratio: unset; /* remove fixed ratio */
}

.plant-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.plant-card__body {
  flex-shrink: 0; /* never compress the text */
  padding: 10px 12px;
}

</style>