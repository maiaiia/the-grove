<script setup>
import {useRouter} from "vue-router";

const props = defineProps({plant: Object})
const router = useRouter()

const goToPlant = () => router.push(`/plant/${props.plant.id}`)
</script>

<template>
  <div class="hero-card" @click="goToPlant">
    <img :src="plant.image" :alt="plant.name" class="hero-card__image" />
    <div class="hero-card__overlay">
      <div class="hero-card__info">
        <h2 class="hero-card__name">{{ plant.name }}</h2>
        <div class="hero-card__meta">
          <span class="hero-card__latin">{{ plant.latinName }}</span>
          <span class="hero-card__age">{{ plant.age }} yrs</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 2 / 3;
  cursor: pointer;

  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.hero-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.hero-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.hero-card:hover .hero-card__image {
  transform: scale(1.04);
}
.hero-card__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(44, 59, 34, 0.85) 10%, transparent 80%);
  display: flex;
  align-items: flex-end;
}

.hero-card__info {
  padding: 28px;
  width: 100%;
}

.hero-card__name {
  font-family: var(--playfair-display), serif;
  font-size: 42px;
  font-weight: 700;
  color: var(--parchment);
  margin: 0 0 8px;
  line-height: 1.1;
}

.hero-card__meta {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.hero-card__latin {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  color: var(--rodeo-dust);
  font-style: italic;
}

.hero-card__age {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  color: var(--rodeo-dust);
}
</style>