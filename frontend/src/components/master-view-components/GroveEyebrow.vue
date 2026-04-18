<script setup>
defineProps({
  count: Number,
  currentView: String,
})
const emit = defineEmits(['update:currentView'])
</script>

<template>
  <div class="eyebrow">
    <div class="eyebrow__left">
      <p class="eyebrow__sub">Your collection · {{ count }} plants</p>
      <h1 class="eyebrow__title">My <em>Grove</em></h1>
    </div>
    <div class="view-toggle">
      <button
          class="toggle-btn"
          :class="{ active: currentView === 'visual' }"
          @click="$emit('update:currentView', 'visual')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-layout-panel-left-icon lucide-layout-panel-left"><rect width="7" height="18" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/></svg>
        VISUAL
      </button>
      <button
          class="toggle-btn"
          :class="{ active: currentView === 'table' }"
          @click="$emit('update:currentView', 'table')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-table-icon lucide-table"><path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/></svg>
        TABLE
      </button>
    </div>
  </div>
</template>

<style scoped>
.eyebrow {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.view-toggle {
  display: flex;
  border: 1px solid var(--rodeo-dust);
  height: 48px;
}
.toggle-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px;
  border: none;
  background: var(--parchment);
  color: var(--mongoose);
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  letter-spacing: 0.2em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-btn.active {
  background: var(--green-kelp);
  color: var(--parchment);
}

.eyebrow__sub {
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--mongoose);
  margin: 0 0 6px;
}

.eyebrow__title {
  font-family: var(--playfair-display), serif;
  font-size: 48px;
  font-weight: 900;
  color: var(--green-kelp);
  margin: 0;
  line-height: 1;
  letter-spacing: -2px;
}

.eyebrow__title em {
  font-style: italic;
  color: var(--marigold);
}

@media (max-width: 768px) {
  .eyebrow {
    display: flex;
    align-items: center;
    flex-direction: column;
    gap: 10px;
  }
}
</style>