<script setup>
import { ref, computed } from 'vue'
import TimelineHistoryItem from '@/components/detail-view-components/TimelineHistoryItem.vue'
import TimelineFeatured from '@/components/detail-view-components/TimelineFeatured.vue'
import { usePlantStore } from '@/stores/plantStore'

const store = usePlantStore()
const props = defineProps({ plant: Object })
const activePhotoIndex = ref(null)

const photos = computed(() => props.plant?.photos || [])

const activePhoto = computed(() => {
  const p = photos.value;
  if (p.length === 0) return null

  const idx = activePhotoIndex.value;
  if (idx === null) return p[p.length - 1]
  return p[idx]
})

function yearsSincePlanted(dateStr) {
  if (!props.plant.datePlanted || !dateStr) return 0;
  const start = new Date(props.plant.datePlanted)
  const photo = new Date(dateStr)
  return Math.floor((photo - start) / (1000 * 60 * 60 * 24 * 365))
}
function handleDeletePhoto(photoId) {
  if (confirm('Are you sure you want to delete this photo?')) { //TODO - use a modal
    store.deletePhoto(photoId)
  }
}
</script>

<template>
  <div class="timeline">
    <p class="timeline__label">Growth Timeline</p>

    <div class="timeline__history" v-if="photos.length">
      <TimelineHistoryItem
          v-for="(photo, i) in photos"
          :key="photo.date"
          :photo="photo"
          :year="yearsSincePlanted(photo.date)"
          :active="activePhoto === photo"
          @click="activePhotoIndex = i"
          @delete="handleDeletePhoto"
      />
    </div>
    <p class="timeline__empty" v-else>No photos yet.</p>

    <TimelineFeatured
        :photo="activePhoto"
        :year="activePhoto ? yearsSincePlanted(activePhoto.date): 0"
        :plant-id="plant.id"
    />
  </div>
</template>

<style scoped>
.timeline {
  background: var(--green-kelp);
  display: flex;
  flex-direction: column;
  padding: 32px;
  gap: 20px;
  overflow: hidden;
}

.timeline__label {
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--avocado);
  margin: 0;
}

.timeline__history {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-right: 8px;
  min-height: 0;
}
.timeline__empty {
  font-family: var(--playfair-display), "Playfair Display", serif;
  font-size: 3vw;
  color: var(--cream);
}
.timeline__history::-webkit-scrollbar { width: 3px; }
.timeline__history::-webkit-scrollbar-track { background: transparent; }
.timeline__history::-webkit-scrollbar-thumb { background: var(--avocado); border-radius: 2px; }
</style>