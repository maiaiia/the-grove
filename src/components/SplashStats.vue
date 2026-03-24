<template>
  <div class="stats">
    <div class="stats__item" v-for="stat in stats" :key="stat.label">
      <span class="stats__number">{{ stat.value }}</span>
      <span class="stats__label">{{ stat.label }}</span>
    </div>
  </div>
</template>

<script setup>
const stats = [
  { value: '2.4k', label: 'users' },
  { value: '18k',  label: 'plants' },
  { value: '50+',  label: 'species' },
]
</script>

<style scoped>
.stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0;
}

.stats__item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding: 28px 0;
  width: 100%;
}

.stats__item + .stats__item {
  border-top: 1px solid rgba(44, 59, 34, 0.15);
}

.stats__number {
  font-family: var(--playfair-display), serif;
  font-size: 32px;
  font-weight: 700;
  color: var(--green-kelp);
  line-height: 1;
}

.stats__label {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--mongoose);
  margin-top: 4px;
}
</style>