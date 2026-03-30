<script setup>
import { computed } from 'vue';

const props = defineProps({
  plants: {
    type: Array,
    required: true
  }
});

const categoryColors = {
  'Bonsai': 'var(--green-kelp)',
  'Tropical': 'var(--avocado)',
  'Flowering': 'var(--marigold)',
  'Succulent': 'var(--clay)',
};

const typeDistribution = computed(() => {
  const counts = {};
  props.plants.forEach(plant => {
    counts[plant.category] = (counts[plant.category] || 0) + 1;
  });

  return Object.entries(counts).map(([type, count]) => ({
    type,
    count,
    color: categoryColors[type] || 'var(--mongoose)'
  }));
});

const segments = computed(() => {
  let cumulative = 0;

  return typeDistribution.value.map(item => {
    const percentage = item.count / totalPlants.value;
    const dash = percentage * 251.2; // circumference (2πr, r=40 → ~251.2)

    const segment = {
      ...item,
      dashArray: `${dash} ${251.2 - dash}`,
      dashOffset: -cumulative
    };

    cumulative += dash;
    return segment;
  });
});

const totalPlants = computed(() => props.plants.length);
</script>

<template>
  <div class="chart-container">
    <p class="chart-label">COLLECTION BREAKDOWN</p>
    <h3 class="chart-title">By plant type</h3>

    <div class="donut-wrapper">
      <div class="donut-chart">
        <svg viewBox="0 0 100 100" class="donut">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#e8e0d0" stroke-width="20"/>
          <circle
              v-for="(segment, index) in segments"
              :key="index"
              cx="50"
              cy="50"
              r="40"
              fill="none"
              :stroke="segment.color"
              stroke-width="20"
              :stroke-dasharray="segment.dashArray"
              :stroke-dashoffset="segment.dashOffset"
              stroke-linecap="butt"
          />
        </svg>
        <div class="donut-center">
          <span class="center-number">{{ totalPlants }}</span>
        </div>
      </div>

      <div class="legend">
        <div v-for="item in typeDistribution" :key="item.type" class="legend-item">
          <div class="legend-dot" :style="{ backgroundColor: item.color }"></div>
          <span class="legend-label">{{ item.type }}</span>
          <span class="legend-count">{{ item.count }}</span>
        </div>
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

.donut-wrapper {
  display: flex;
  align-items: center;
  gap: 40px;
}

.donut-chart {
  position: relative;
  width: 160px;
  height: 160px;
  flex-shrink: 0;
}

.donut {
  transform: rotate(-90deg);
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--playfair-display), "Playfair Display", serif;
}

.center-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--green-kelp);
}

.legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label {
  font-size: 14px;
  color: var(--green-kelp);
  flex: 1;
}

.legend-count {
  font-size: 13px;
  color: var(--mongoose);
  font-weight: 500;
}

</style>