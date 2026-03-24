<script setup>
defineProps({ plant: Object })
</script>

<template>
  <div class="plant-card">
    <div class="plant-card__image-wrapper">
      <img :src="plant.image" :alt="plant.name" class="plant-card__image" />
    </div>
    <div class="plant-card__body">
      <div class="plant-card__row">
        <h3 class="plant-card__name">{{ plant.name }}</h3>
        <span class="plant-card__age">{{ plant.age }} yrs</span>
      </div>
      <p class="plant-card__latin">{{ plant.latinName }}</p>
    </div>
  </div>
</template>

<style scoped>
.plant-card {
  background: var(--parchment);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
}

.plant-card__image-wrapper {
  aspect-ratio: 4 / 3;
  overflow: hidden;
}

.plant-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.plant-card:hover .plant-card__image {
  transform: scale(1.04);
}

.plant-card__body {
  padding: 14px 16px;
}

.plant-card__row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4px;
}

.plant-card__name {
  font-family: var(--playfair-display), serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--green-kelp);
  margin: 0;
}

.plant-card__age {
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  color: var(--mongoose);
}

.plant-card__latin {
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  color: var(--avocado);
  font-style: italic;
  margin: 0;
}
</style>