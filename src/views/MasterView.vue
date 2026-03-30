<script setup>
import { ref, computed, watch } from 'vue'
import { usePlantStore } from '@/stores/plantStore'
import AppNav from "@/components/AppNav.vue"
import GroveEyebrow from "@/components/master-view-components/GroveEyebrow.vue"
import GrovePagination from "@/components/master-view-components/GrovePagination.vue"
import GroveVisual from "@/components/master-view-components/GroveVisual.vue"
import GroveTable from "@/components/master-view-components/GroveTable.vue"

const store = usePlantStore()
const viewMode = ref('visual')
const currentPage = ref(1)

const perPage = computed(() => viewMode.value === 'visual' ? 5 : 10)
const totalPages = computed(() => Math.ceil(store.plants.length / perPage.value))

watch(viewMode, () => currentPage.value = 1)

const paginatedPlants = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return store.plants.slice(start, start + perPage.value)
})

const heroPlant = computed(() => paginatedPlants.value[0])
const gridPlants = computed(() => paginatedPlants.value.slice(1))


const handleSelect = (plant) => {
  console.log('Navigate to detail for:', plant.name)
}
</script>

<template>
  <div class="grove">
    <AppNav class="grove__nav" />

    <div class="grove__inner">
      <GroveEyebrow
          :count="store.plants.length"
          v-model:currentView="viewMode"
      />

      <GroveVisual
          v-if="viewMode === 'visual'"
          :hero-plant="heroPlant"
          :grid-plants="gridPlants"
      />

      <GroveTable
          v-else
          :plants="paginatedPlants"
          @select="handleSelect"
      />

      <GrovePagination
          :current="currentPage"
          :total="totalPages"
          :total-items="store.plants.length"
          :items-per-page="perPage"
          @change="currentPage = $event"
      />
    </div>
  </div>
</template>

<style scoped>
.grove {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--parchment);
  overflow-y: auto;
}

.grove__inner {
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  gap: 24px;
}

@media (min-width: 1024px) {
  .grove {
    height: 100vh;
    overflow: hidden;
  }

  .grove__inner {
    padding: 24px 48px;
    justify-content: space-between;
  }
}
</style>