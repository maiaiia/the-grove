<script setup>

</script>

<template>
  <div class="breadcrumb">
    <router-link to="/grove">My Grove</router-link>
    <span>/</span>
    <span>Statistics</span>
  </div>
</template>

<style scoped>
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 48px;
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--mongoose);
  border-bottom: 1px solid rgba(44, 59, 34, 0.08);
}

.breadcrumb a {
  color: var(--mongoose);
  text-decoration: none;
}

.breadcrumb a:hover { color: var(--green-kelp); }
</style>