<script setup>
import {computed} from "vue";

const props = defineProps({
  current: Number,
  total: Number,
  itemsPerPage: {type: Number, default: 5},
  totalItems: Number
})
const emit = defineEmits(['change'])

const pages = computed(() => {
  return Array.from({ length: props.total }, (_, i) => i + 1)
})

const rangeLabel = computed(() => {
  const start = (props.current - 1) * props.itemsPerPage + 1
  const end = Math.min(props.current * props.itemsPerPage, props.totalItems)
  return `${start}–${end} of ${props.totalItems}`
})
</script>

<template>
  <div class="pagination">
    <button class="pagination__arrow" :disabled="current === 1" @click="emit('change', current - 1)">‹</button>
    <button
        v-for="p in pages"
        :key="p"
        class="pagination__page"
        :class="{ active: p === current }"
        @click="emit('change', p)"
    >{{ p }}</button>
    <span class="pagination__info">{{ rangeLabel }}</span>
    <button class="pagination__arrow" :disabled="current === total" @click="emit('change', current + 1)">›</button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.pagination__arrow,
.pagination__page {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  width: 36px;
  height: 36px;
  border: 1px solid var(--rodeo-dust);
  background: transparent;
  color: var(--green-kelp);
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination__page.active {
  background: var(--green-kelp);
  color: var(--parchment);
  border-color: var(--green-kelp);
}

.pagination__arrow:disabled {
  opacity: 0.3;
  cursor: default;
}

.pagination__info {
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  color: var(--mongoose);
  letter-spacing: 0.08em;
  padding: 0 8px;
}
</style>