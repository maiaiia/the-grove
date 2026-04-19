<script setup>
import { computed } from 'vue';

const props = defineProps({
  wateringDistribution: {
    type: Array,
    required: true,
    default: () => []
  }
});

const frequencyData = computed(() => {
  if (!props.wateringDistribution.length) return [];
  const maxCount = Math.max(...props.wateringDistribution.map(d => d.count), 1);
  return props.wateringDistribution.map((item)=>({
    ...item,
    count:item.length,
    percentage: (item.count / maxCount) * 100
  }))
});

const locationData = computed(() => {
  const locations = {};

  props.plants.forEach(plant => {
    locations[plant.location] = (locations[plant.location] || 0) + 1;
  });

  const maxCount = Math.max(...Object.values(locations), 1);

  return Object.entries(locations).map(([location, count]) => ({
    location,
    count,
    percentage: (count / maxCount) * 100
  }));
});
</script>

<template>
  <div class="chart-container">
    <p class="chart-label">CARE INSIGHTS</p>
    <h3 class="chart-title">Watering frequency</h3>

    <div class="frequency-section">
      <div v-for="item in frequencyData" :key="item.label" class="frequency-row">
        <span class="frequency-label">{{ item.label }}</span>
        <div class="bar-container">
          <div
              class="bar"
              :style="{ width: `${item.percentage}%` }"
          ></div>
        </div>
        <span class="frequency-count">{{ item.count }}</span>
      </div>
    </div>
  <!--
    <div class="location-section">
      <p class="section-label">LOCATION SPLIT</p>
      <div v-for="item in locationData" :key="item.location" class="frequency-row">
        <span class="frequency-label">{{ item.location }}</span>
        <div class="bar-container">
          <div
              class="bar location-bar"
              :style="{ width: `${item.percentage}%` }"
          ></div>
        </div>
        <span class="frequency-count">{{ item.count }}</span>
      </div>
    </div>
    -->
  </div>
</template>

<style scoped>
.chart-container {
  background-color: var(--grayish);
  padding: 32px;
  border-radius: 2px;
}

.chart-label {
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--mongoose);
  margin-bottom: 8px;
  font-weight: 500;
}

.chart-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--green-kelp);
  margin-bottom: 32px;
  font-family: 'Playfair Display', serif;
}

.frequency-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 40px;
}

.location-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-label {
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--mongoose);
  margin-bottom: 16px;
  font-weight: 500;
}

.frequency-row {
  display: grid;
  grid-template-columns: 140px 1fr 40px;
  align-items: center;
  gap: 16px;
}

.frequency-label {
  font-size: 13px;
  color: var(--green-kelp);
  font-weight: 400;
}

.bar-container {
  height: 24px;
  background-color: rgba(139, 115, 85, 0.1);
  border-radius: 1px;
  overflow: hidden;
}

.bar {
  height: 100%;
  background-color: #8b7355;
  transition: width 0.6s ease;
  border-radius: 1px;
}

.location-bar {
  background-color: #5a7a56;
}

.frequency-count {
  font-size: 12px;
  color: var(--mongoose);
  text-align: right;
}
</style>