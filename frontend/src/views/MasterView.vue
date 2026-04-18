<script setup>
import {ref, computed, watch, onMounted} from 'vue'
import { usePlantStore } from '@/stores/plantStore.js'
import AppNav from "@/components/AppNav.vue"
import GroveEyebrow from "@/components/master-view-components/GroveEyebrow.vue"
import GrovePagination from "@/components/master-view-components/GrovePagination.vue"
import GroveVisual from "@/components/master-view-components/GroveVisual.vue"
import GroveTable from "@/components/master-view-components/GroveTable.vue"
import { getCookie, setCookie } from "@/utils/cookieHelper.js";

const store = usePlantStore()
onMounted(() => store.fetchPlants())
const savedView = getCookie('grove_view')
const viewMode = ref(savedView || 'visual')
const previousPageNumber = getCookie('previousPageNumber')
const currentPage = ref( previousPageNumber || 1)

const perPage = computed(() => viewMode.value === 'visual' ? 5 : 10)
const totalPages = computed(() => Math.ceil(store.plants.length / perPage.value))

watch(viewMode, (newVal) => {
  setCookie('grove_view', newVal);
  currentPage.value = 1;
})
watch(currentPage, (newVal) =>{
  setCookie('previousPageNumber', newVal);
})

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
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: var(--parchment);
}

.grove__inner {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 24px 48px;
  gap: 20px;
  min-height: 0;
}
</style>