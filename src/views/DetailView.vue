<script setup>
import { useRoute } from 'vue-router'
import { usePlantStore } from '@/stores/plantStore'
import { computed } from 'vue'
import AppNav from '@/components/AppNav.vue'
import DetailBreadcrumb from '@/components/detail-view-components/DetailBreadcrumb.vue'
import PlantTimeline from '@/components/detail-view-components/PlantTimeline.vue'
import PlantProfile from '@/components/detail-view-components/PlantProfile.vue'

const route = useRoute()
const store = usePlantStore()
const plant = computed(() => store.plants.find(p => p.id == route.params.id))
</script>

<template>
  <div class="detail" v-if="plant">
    <AppNav />
    <DetailBreadcrumb :plant-name="plant.name" />
    <div class="detail__body">
      <PlantTimeline :plant="plant" />
      <PlantProfile :plant="plant" />
    </div>
  </div>
</template>

<style scoped>
.detail {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-background);
  overflow: hidden;
}

.detail__body {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 0;
}
</style>