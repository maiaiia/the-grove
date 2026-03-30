<script setup>
import {computed, useCssVars} from "vue";

const props = defineProps({
  theme: {type: String, default: 'light' }
})
const textColor = computed(() => props.theme === 'dark' ? 'var(--parchment)' : 'var(--mongoose)');
</script>

<template>
  <p class="description">
    Document every leaf, every season, every slow transformation.
    Share your grove, connect with fellow gardeners, and watch your
    collection take shape over time.
  </p>
</template>

<style scoped>
.description {
  font-family: var(--space-mono), monospace;
  font-size: 13px;
  line-height: 1.9;
  color: v-bind(textColor);
  border-left: 2px solid var(--marigold);
  padding-left: 16px;
  margin: 0;
  max-width: 340px;
}
</style>