<script setup>
defineProps({ count: Number })
</script>

<template>
  <div class="eyebrow">
    <p class="eyebrow__sub">Your collection · {{ count }} plants</p>
    <h1 class="eyebrow__title">My <em>Grove</em></h1>
  </div>
</template>

<style scoped>
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
</style>