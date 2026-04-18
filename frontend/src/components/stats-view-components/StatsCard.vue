<script setup>
defineProps({
  label: String,
  value: [String, Number],
  sublabel: String
});
</script>

<template>
  <div class="stats-card">
    <p class="card-label">{{ label }}</p>
    <div class="card-value-container">
      <h2 class="card-value">{{ value }}</h2>
      <span v-if="sublabel" class="card-sublabel">{{ sublabel }}</span>
    </div>
  </div>
</template>

<style scoped>
.stats-card {
  background-color: var(--grayish);
  margin: 1px;
  border-color: var(--mongoose);
  padding: 24px;
  border-radius: 2px;
}

.card-label {
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--mongoose);
  margin-bottom: 12px;
  font-weight: 500;
}

.card-value-container {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.card-value {
  font-size: 48px;
  font-weight: 700;
  color: var(--green-kelp);
  line-height: 1;
  font-family: var(--playfair-display), 'Playfair Display', serif;
}

.card-sublabel {
  font-size: 16px;
  color: var(--mongoose);
  font-weight: 400;
}
</style>