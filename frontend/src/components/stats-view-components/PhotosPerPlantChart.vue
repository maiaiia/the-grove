<script setup>
import { computed } from 'vue';

const props = defineProps({
  plants: {
    type: Array,
    required: true
  }
});

// Group plants by photo count brackets
const photoDistribution = computed(() => {
  const brackets = [
    { label: '0 photos', min: 0, max: 0 },
    { label: '1-2 photos', min: 1, max: 2 },
    { label: '3-5 photos', min: 3, max: 5 },
    { label: '6-10 photos', min: 6, max: 10 },
    { label: '10+ photos', min: 11, max: Infinity }
  ];

  const colors = ['#2d3d2b', '#3d5a3a', '#5a7a56', '#8b7355', '#a89b7e'];

  const distribution = brackets.map((bracket, index) => {
    const plantsInBracket = props.plants.filter(plant => {
      const photoCount = plant.photos?.length || 0;
      return photoCount >= bracket.min && (bracket.max === Infinity ? true : photoCount <= bracket.max);
    });

    return {
      ...bracket,
      count: plantsInBracket.length,
      color: colors[index]
    };
  }).filter(d => d.count > 0); // Only show brackets with plants

  const maxCount = Math.max(...distribution.map(d => d.count), 1);

  return distribution.map(d => ({
    ...d,
    percentage: (d.count / maxCount) * 100
  }));
});
</script>

<template>
  <div class="chart-container">
    <p class="chart-label">DOCUMENTATION LEVEL</p>
    <h3 class="chart-title">Photos per plant</h3>

    <div class="photo-bars">
      <div v-for="bracket in photoDistribution" :key="bracket.label" class="photo-bar-row">
        <span class="photo-label">{{ bracket.label }}</span>
        <div class="bar-container">
          <div
              class="bar"
              :style="{
              width: `${bracket.percentage}%`,
              backgroundColor: bracket.color
            }"
          ></div>
        </div>
        <span class="photo-count">{{ bracket.count }}</span>
      </div>
    </div>
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

.photo-bars {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.photo-bar-row {
  display: grid;
  grid-template-columns: 120px 1fr 40px;
  align-items: center;
  gap: 16px;
}

.photo-label {
  font-size: 13px;
  color: var(--green-kelp);
  font-weight: 400;
}

.bar-container {
  height: 28px;
  background-color: rgba(139, 115, 85, 0.1);
  border-radius: 1px;
  overflow: hidden;
}

.bar {
  height: 100%;
  transition: width 0.6s ease;
  border-radius: 1px;
}

.photo-count {
  font-size: 12px;
  color: var(--mongoose);
  text-align: right;
}
</style>