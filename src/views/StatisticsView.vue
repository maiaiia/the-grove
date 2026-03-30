<script setup>
import { computed } from 'vue';
import StatsCard from "@/components/stats-view-components/StatsCard.vue";
import PlantAgesChart from "@/components/stats-view-components/PlantAgesChart.vue";
import PhotosPerPlantChart from "@/components/stats-view-components/PhotosPerPlantChart.vue";
import PlantTypeChart from "@/components/stats-view-components/PlantTypeChart.vue";
import {usePlantStore} from "@/stores/plantStore.js";
import AppNav from "@/components/AppNav.vue";
import StatsBreadcrumb from "@/components/stats-view-components/StatsBreadcrumb.vue";
import WateringFrequency from "@/components/stats-view-components/WateringFrequency.vue";

const plants = usePlantStore().plants

const totalPlants = computed(() => plants.length);

const oldestPlant = computed(() => {
  if (!plants.length) return { age: 0 };
  return plants.reduce((oldest, plant) =>
      plant.age > oldest.age ? plant : oldest
  );
});

const totalPhotos = computed(() => {
  return plants.reduce((sum, plant) =>
      sum + (plant.photos?.length || 0), 0
  );
});

const avgPhotosPerPlant = computed(() => {
  if (!plants.length) return 0;
  return Math.round(totalPhotos.value / plants.value.length);
});

const uniqueLocations = computed(() => {
  return new Set(plants.map(p => p.location)).size;
});
</script>

<template>

  <AppNav />
  <StatsBreadcrumb />
  <div class="statistics-page">

    <div class="page-header">
      <div>
        <p class="page-subtitle">YOUR GROVE AT A GLANCE</p>
        <h1 class="page-title">Grove <em>Statistics</em></h1>
      </div>
    </div>

    <div class="stats-grid">
      <StatsCard
          label="TOTAL PLANTS"
          :value="totalPlants"
          sublabel="and growing"
      />
      <StatsCard
          label="OLDEST PLANT"
          :value="oldestPlant.age"
          sublabel="yrs"
      />
      <StatsCard
          label="UNIQUE LOCATIONS"
          :value="uniqueLocations"
          sublabel="spots"
      />
      <StatsCard
          label="TOTAL PHOTOS TAKEN"
          :value="plants.reduce((sum, p)=> sum + p.photos.length, 0)"
          sublabel="photos"
      />
    </div>


    <div class="charts-grid">
      <PlantAgesChart :plants="plants" />
      <PlantTypeChart :plants="plants" />
      <PhotosPerPlantChart :plants="plants" />
      <WateringFrequency :plants="plants" />
    </div>
  </div>
</template>

<style scoped>
* {
  font-family: var(--space-mono), monospace;
}

.statistics-page {
  padding: 40px 60px;
  background-color: var(--parchment);
  min-height: 100vh;
}

.page-header {
  margin-bottom: 40px;
}

.page-subtitle {
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--mongoose);
  margin-bottom: 8px;
  font-weight: 500;
}

.page-title {
  font-size: 52px;
  font-weight: 700;
  color: var(--green-kelp);
  font-family: 'Playfair Display', serif;
}

.page-title em {
  font-style: italic;
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  color: var(--marigold)
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>