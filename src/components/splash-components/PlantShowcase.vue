<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePlantStore } from '@/stores/plantStore.js'

defineProps({
  maxWidth: {
    type: String,
    default: '900px'
  }
})

const store = usePlantStore()
const currentIndex = ref(0)
const currentPlant = computed(() => store.plants[currentIndex.value])

let interval
onMounted(() => {
  interval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % store.plants.length
  }, 5000)
})
onUnmounted(() => clearInterval(interval))

const seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
const currentYear = new Date().getFullYear()
const month = new Date().getMonth()
const seasonIndex = Math.floor(((month + 1) % 12) / 3) /*TODO -- compute season via lastPhoto*/
const currentSeason = seasons[seasonIndex]
</script>

<template>
  <div class="plant-showcase" :style="{ maxWidth }">
    <div class="plant-ring plant-ring--inner" />
    <div class="plant-ring plant-ring--outer" />
    <div class="plant-image-wrapper">
      <img :src="currentPlant.image" :alt="currentPlant.name" class="plant-image" />
    </div>

    <div class="plant-card">
      <span class="plant-card__label">Currently featuring</span>
      <h2 class="plant-card__name">
        {{ currentPlant.name.split(' ')[0] }}
        <em>{{ currentPlant.name.split(' ').slice(1).join(' ') }}</em>
      </h2>
      <p class="plant-card__meta">{{ currentPlant.latinName }} · {{ currentPlant.age }} years</p>
    </div>

    <div class="plant-season">
      <div class="plant-season__tag">
        <span class="dot"></span>
        <span class="plant-season__label">{{ currentSeason }} {{ currentYear }}</span>
      </div>
      <div class="plant-season__dots">
        <span
            v-for="(_, i) in store.plants.length"
            :key="i"
            class="dot"
            :class="{ active: i === currentIndex }"
            @click="currentIndex = i"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>

.plant-showcase {
  position: relative;
  width: 100%;
  max-width: 900px;
  aspect-ratio: 4 / 3;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.plant-image-wrapper {
  width: 70%;
  aspect-ratio: 1;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
  margin-left: 8%;
}

.plant-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.plant-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid var(--marigold);
  top: 50%;
  left: 54%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 0;
}

.plant-ring--inner {
  width: 75%;
  aspect-ratio: 1;
  opacity: 0.3;
}

.plant-ring--outer {
  width: 80%;
  border-width: 2px;
  aspect-ratio: 1;
  opacity: 0.1;
}
.plant-card {
  position: absolute;
  left: 0;
  bottom: 22%;
  background: var(--green-kelp);
  color: #fff;
  padding: 20px 28px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 300px;

  font-family: var(--space-mono), "Space Mono", monospace;
  text-transform: uppercase;
}

.plant-card__label {
  font-size: 8px;
  text-transform: uppercase;
  color: var(--marigold);
  letter-spacing: 1.75px;

  line-height: normal;
  font-weight: 400;
}

.plant-card__name {
  font-size: 18px;
  font-weight: 700;
  color: var(--parchment);
  margin: 0;
  line-height: 20px;

  font-family: var(--playfair-display), "Playfair Display", serif;
  text-transform: none;
}

.plant-card__name em {
  font-style: italic;
  color: var(--marigold);
}

.plant-card__meta {
  color: var(--parchment, rgba(240, 233, 214, 0.40));
  /* Space Mono/Regular */
  font-family: var(--space-mono, "Space Mono"), monospace;
  font-size: 9px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 0.9px;
  opacity: 0.5;
}

.plant-season {
  position: absolute;
  bottom: 6%;
  right: 8%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.plant-season__tag {
  display: flex;
  align-items: center;
  gap: 6px;
}

.plant-season__label {
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #4a4a4a;
  font-weight: 500;
}

.plant-season__dots {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 10px;
}

.dot {
  display: block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(0,0,0,0.15);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  flex-shrink: 0;
}

.plant-season__tag .dot {
  background: var(--marigold);
  width: 8px;
  height: 8px;
}

.plant-season__dots .dot.active {
  width: 24px;
  border-radius: 10px;

  background: linear-gradient(
      to right,
      var(--marigold) 50%,
      rgba(0, 0, 0, 0.15) 50%
  );

  background-size: 200% 100%;
  background-position: 100% 0;

  animation: fill-progress 5s linear infinite;
}

@keyframes fill-progress {
  0% {
    background-position: 100% 0;
  }
  100% {
    background-position: 0% 0;
  }
}
</style>