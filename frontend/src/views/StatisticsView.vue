<script setup>
import {computed, onMounted} from 'vue';
import StatsCard from "@/components/stats-view-components/StatsCard.vue";
import PlantAgesChart from "@/components/stats-view-components/PlantAgesChart.vue";
import PhotosPerPlantChart from "@/components/stats-view-components/PhotosPerPlantChart.vue";
import PlantTypeChart from "@/components/stats-view-components/PlantTypeChart.vue";
import {usePlantStore} from "@/stores/plantStore.js";
import AppNav from "@/components/AppNav.vue";
import StatsBreadcrumb from "@/components/stats-view-components/StatsBreadcrumb.vue";
import WateringFrequency from "@/components/stats-view-components/WateringFrequency.vue";

const store = usePlantStore();
onMounted(()=>store.fetchPlantStatistics());
const stats = computed(() => store.stats);

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
          :value="stats.totalPlants"
          sublabel="and growing"
      />
      <StatsCard
          label="OLDEST PLANT"
          :value="stats.oldestPlant"
          sublabel="yrs"
      />
      <StatsCard
          label="UNIQUE LOCATIONS"
          :value="stats.uniqueLocations"
          sublabel="spots"
      />
      <StatsCard
          label="TOTAL PHOTOS TAKEN"
          :value="stats.totalPhotos"
          sublabel="photos"
      />
    </div>

    <div class="charts-grid">
      <PlantAgesChart :ageDistribution="stats.ageDistribution" />
      <PlantTypeChart :typeDistribution="stats.typeDistribution"
                      :totalPlants="stats.totalPlants" />
    <!--
      <PhotosPerPlantChart :plants="plants" />
      <WateringFrequency :plants="plants" />
      -->
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

.charts-grid > * {
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
  box-sizing: border-box;
}
.charts-grid :deep(canvas),
.charts-grid :deep(svg) {
  max-width: 100% !important;
  height: auto !important;
}

.charts-grid :deep(> div) {
  max-width: 100%;
  overflow: hidden;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .statistics-page {
    padding: 20px 16px;
  }

  .page-title {
    font-size: 36px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

}
</style>