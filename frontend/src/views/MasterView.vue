<script setup>
import {ref, computed, watch, onMounted} from 'vue'
import { usePlantStore } from '@/stores/plantStore.js'
import AppNav from "@/components/AppNav.vue"
import GroveEyebrow from "@/components/master-view-components/GroveEyebrow.vue"
import GrovePagination from "@/components/master-view-components/GrovePagination.vue"
import GroveVisual from "@/components/master-view-components/GroveVisual.vue"
import GroveTable from "@/components/master-view-components/GroveTable.vue"
import { getCookie, setCookie } from "@/utils/cookieHelper.js"

const store = usePlantStore()
const savedView = getCookie('grove_view')
const viewMode = ref(savedView || 'visual')
const previousPageNumber = getCookie('previousPageNumber')
const visualPage = ref(previousPageNumber ? parseInt(previousPageNumber) : 1)

// Visual mode: display 5 items per "page" (UI pagination)
const visualPerPage = 5
const totalVisualPages = computed(() => Math.ceil(store.totalPlants / visualPerPage))

// Initialize
onMounted(async () => {
  await store.fetchPage(1, false)
})

// Watch view mode changes
watch(viewMode, async (newVal) => {
  setCookie('grove_view', newVal)

  if (newVal === 'visual') {
    store.resetPages()
    visualPage.value = 1
    await store.fetchPage(1, false)
  } else {
    store.resetPages()
    await store.fetchPage(1, false)
  }
})

// Watch visual page changes
watch(visualPage, async (newPage) => {
  setCookie('previousPageNumber', newPage)

  // Calculate which server page(s) we need for this visual page
  const startIndex = (newPage - 1) * visualPerPage
  const endIndex = startIndex + visualPerPage
  const startServerPage = Math.floor(startIndex / store.pageSize) + 1
  const endServerPage = Math.floor(endIndex / store.pageSize) + 1

  // Fetch any missing pages
  for (let page = startServerPage; page <= endServerPage; page++) {
    await store.fetchPage(page, page > 1) // append if not first page
  }
})

// Plants for visual mode (sliced from store)
const visualPaginatedPlants = computed(() => {
  const start = (visualPage.value - 1) * visualPerPage
  return store.plants.slice(start, start + visualPerPage)
})

const heroPlant = computed(() => visualPaginatedPlants.value[0])
const gridPlants = computed(() => visualPaginatedPlants.value.slice(1))

// Handle infinite scroll for table view
const handleLoadMore = async () => {
  const nextPage = Math.floor(store.plants.length / store.pageSize) + 1
  const hasMore = await store.fetchPage(nextPage, true)
  return hasMore
}

const handleSelect = (plant) => {
  console.log('Navigate to detail for:', plant.name)
}
</script>

<template>
  <div class="grove">
    <AppNav class="grove__nav" />

    <div class="grove__inner">
      <GroveEyebrow
          :count="store.totalPlants"
          v-model:currentView="viewMode"
      />

      <GroveVisual
          v-if="viewMode === 'visual'"
          :hero-plant="heroPlant"
          :grid-plants="gridPlants"
      />

      <GroveTable
          v-else
          :plants="store.plants"
          @select="handleSelect"
          @load-more="handleLoadMore"
      />

      <GrovePagination
          v-if="viewMode === 'visual'"
          :current="visualPage"
          :total="totalVisualPages"
          :total-items="store.totalPlants"
          :items-per-page="visualPerPage"
          @change="visualPage = $event"
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