<script setup>
defineProps({ photo: Object, year: Number, active: Boolean })
defineEmits(['click'])

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-GB', {
    month: 'long', year: 'numeric'
  })
}
</script>

<template>
  <div class="history-item" :class="{ active }" @click="$emit('click')">
    <div class="history-item__dot" />
    <img v-if="photo" :src="photo.url" class="history-item__thumb" />
    <div v-else class="history-item__thumb history-item__thumb--placeholder">
      <img src="/grovelogo.svg" style="width: 24px; opacity: 0.3;" />
    </div>
    <div class="history-item__meta">
      <span class="history-item__desc">{{ photo.description || '—' }}</span>
      <span class="history-item__date">{{ formatDate(photo.date) }}</span>
      <span class="history-item__year">Year {{ year }}</span>
    </div>
  </div>
</template>

<style scoped>
.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.history-item:hover,
.history-item.active { opacity: 1; }

.history-item__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1px solid var(--avocado);
  flex-shrink: 0;
  transition: background 0.2s, border-color 0.2s;
}

.history-item.active .history-item__dot {
  background: var(--marigold);
  border-color: var(--marigold);
}

.history-item__thumb {
  width: 64px;
  height: 48px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
}

.history-item__meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.history-item__desc {
  font-family: var(--playfair-display), serif;
  font-size: 13px;
  color: var(--parchment);
}

.history-item__date {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  letter-spacing: 0.08em;
  color: var(--avocado);
  text-transform: uppercase;
}

.history-item__year {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  color: var(--marigold);
  text-transform: uppercase;
}
.history-item__thumb--placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.05);
}
</style>