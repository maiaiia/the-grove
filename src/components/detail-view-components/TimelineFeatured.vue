<script setup>
defineProps({ photo: Object, year: Number })

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-GB', {
    month: 'long', year: 'numeric'
  })
}
</script>

<template>
  <div class="featured">
    <div class="featured__label">
      <span class="featured__tag">Most Recent</span>
      <span class="featured__date">{{ formatDate(photo.date) }}</span>
    </div>
    <div class="featured__image-wrapper">
      <img :src="photo.url" class="featured__image" />
      <div class="featured__overlay">
        <span class="featured__desc">{{ photo.description || '—' }}</span>
        <span class="featured__year">Year {{ year }}</span>
      </div>
    </div>
    <button class="featured__add">+ Add new photo</button>
  </div>
</template>

<style scoped>
.featured {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.featured__label {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.featured__tag {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--marigold);
}

.featured__date {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  color: var(--avocado);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.featured__image-wrapper {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 16 / 9;
}

.featured__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.featured__overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  background: linear-gradient(to top, rgba(20, 30, 15, 0.85), transparent);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.featured__desc {
  font-family: var(--playfair-display), serif;
  font-size: 14px;
  color: var(--parchment);
}

.featured__year {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  color: var(--marigold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.featured__add {
  background: none;
  border: 1px dashed rgba(255,255,255,0.2);
  color: var(--avocado);
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  letter-spacing: 0.1em;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  text-transform: uppercase;
  transition: border-color 0.2s, color 0.2s;
}

.featured__add:hover {
  border-color: var(--marigold);
  color: var(--marigold);
}
</style>