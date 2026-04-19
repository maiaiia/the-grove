<script setup>
import { computed } from 'vue';

const props = defineProps({
  ageDistribution: {
    type: Array,
    required: true,
    default: () => []
  }
});

const processedData = computed(() => {
  if (!props.ageDistribution.length) return [];

  const maxCount = Math.max(...props.ageDistribution.map(d => d.count), 1);

  return props.ageDistribution.map(item => ({
    ...item,
    percentage: (item.count / maxCount) * 100
  }));
});
</script>

<template>
  <div class="chart-container">
    <p class="chart-label">GROWTH TIMELINE</p>
    <h3 class="chart-title">Plant ages</h3>

    <div class="age-bars">
      <div v-for="bracket in processedData" :key="bracket.label" class="age-bar-row">
        <span class="age-label">{{ bracket.label }}</span>
        <div class="bar-container">
          <div
              class="bar"
              :style="{ width: `${bracket.percentage}%` }"
          ></div>
        </div>
        <span class="age-count">{{ bracket.count }}</span>
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

.age-bars {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.age-bar-row {
  display: grid;
  grid-template-columns: 60px 1fr 40px;
  align-items: center;
  gap: 16px;
}

.age-label {
  font-size: 13px;
  color: var(--green-kelp);
  font-weight: 500;
}

.bar-container {
  height: 24px;
  background-color: rgba(139, 115, 85, 0.1);
  border-radius: 1px;
  overflow: hidden;
}

.bar {
  height: 100%;
  transition: width 0.6s ease;
  border-radius: 1px;
  background-color: var(--avocado);
}

.age-count {
  font-size: 12px;
  color: var(--mongoose);
  text-align: right;
}
</style>