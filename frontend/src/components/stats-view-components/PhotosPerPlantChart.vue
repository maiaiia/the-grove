<script setup>
import { computed } from 'vue';

const props = defineProps({
  photoDistribution: {
    type: Array,
    required: true,
    default: () => []
  }
});

const chartData = computed(() => {
  if (!props.photoDistribution.length) return [];
  const colors = ['#2d3d2b', '#3d5a3a', '#5a7a56', '#8b7355', '#a89b7e'];
  const maxCount = Math.max(...props.photoDistribution.map(d => d.count), 1);
  return props.photoDistribution.map((item, index) => ({
    ...item,
    color: colors[index % colors.length],
    percentage: (item.count / maxCount) * 100
  }));
});
</script>

<template>
  <div class="chart-container">
    <p class="chart-label">DOCUMENTATION LEVEL</p>
    <h3 class="chart-title">Photos per plant</h3>

    <div class="photo-bars">
      <div v-for="bracket in chartData" :key="bracket.label" class="photo-bar-row">
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