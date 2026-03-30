<script setup>
import { computed } from 'vue';

const props = defineProps({
  plants: {
    type: Array,
    required: true
  }
});

const ageBrackets = [
  { label: '<1y', min: 0, max: 1},
  { label: '1-2y', min: 1, max: 2},
  { label: '2-5y', min: 2, max: 5},
  { label: '5-10y', min: 5, max: 10},
  { label: '10-25y', min: 10, max: 25},
  { label: '25y+', min: 25, max: Infinity}
];

const ageDistribution = computed(() => {
  const distribution = ageBrackets.map(bracket => ({
    ...bracket,
    count: props.plants.filter(plant => {
      const age = plant.age;
      return age >= bracket.min && (bracket.max === Infinity ? true : age < bracket.max);
    }).length
  }));

  const maxCount = Math.max(...distribution.map(d => d.count), 1);

  return distribution.map(d => ({
    ...d,
    percentage: (d.count / maxCount) * 100
  }));
});
</script>

<template>
  <div class="chart-container">
    <p class="chart-label">GROWTH TIMELINE</p>
    <h3 class="chart-title">Plant ages</h3>

    <div class="age-bars">
      <div v-for="bracket in ageDistribution" :key="bracket.label" class="age-bar-row">
        <span class="age-label">{{ bracket.label }}</span>
        <div class="bar-container">
          <div
              class="bar"
              :style="{
              width: `${bracket.percentage}%`,
            }"
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