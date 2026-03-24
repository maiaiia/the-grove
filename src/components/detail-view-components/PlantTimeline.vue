<script setup>
import { ref, computed } from 'vue'
import TimelineHistoryItem from '@/components/detail-view-components/TimelineHistoryItem.vue'
import TimelineFeatured from '@/components/detail-view-components/TimelineFeatured.vue'

const props = defineProps({ plant: Object })

const activePhotoIndex = ref(null)

const sortedPhotos = computed(() => props.plant.sortedPhotos || [])

const activePhoto = computed(() => {
  const photos = sortedPhotos.value
  if (!photos.length) return null
  if (activePhotoIndex.value === null) return photos[photos.length - 1]
  return photos[activePhotoIndex.value]
})

function yearsSincePlanted(dateStr) {
  const start = new Date(props.plant.datePlanted)
  const photo = new Date(dateStr)
  return Math.floor((photo - start) / (1000 * 60 * 60 * 24 * 365))
}
</script>

<template>
  <div class="timeline">
    <p class="timeline__label">Growth Timeline</p>

    <div class="timeline__history">
      <TimelineHistoryItem
          v-for="(photo, i) in sortedPhotos"
          :key="photo.date"
          :photo="photo"
          :year="yearsSincePlanted(photo.date)"
          :active="activePhoto === photo"
          @click="activePhotoIndex = i"
      />
    </div>

    <TimelineFeatured
        :photo="activePhoto"
        :year="yearsSincePlanted(activePhoto.date)"
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

.timeline__history::-webkit-scrollbar { width: 3px; }
.timeline__history::-webkit-scrollbar-track { background: transparent; }
.timeline__history::-webkit-scrollbar-thumb { background: var(--avocado); border-radius: 2px; }
</style>