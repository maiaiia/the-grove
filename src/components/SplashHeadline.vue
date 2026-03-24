<script setup>

</script>

<template>
  <div class="headline">
    <div class="description-short">
      <div class="divider"/>
      <p> A living plant journal</p>
    </div>
    <div class="logo">
      <img src="/src/assets/logo-transparent.svg" width="160px" height="160px" alt="logo">
      <div class="brand">
        <p>The</p>
        <p><i><b>Grove</b></i></p>
      </div>
    </div>
    <div class="tagline">
      <div class="tagline-dots">
        <div class="dot" />
        <div class="dot" />
        <div class="dot" />
      </div>
      <p> Every leaf, a new season</p>
    </div>

  </div>
</template>

<style scoped>
* {

}

.headline{
  display: flex;
  flex-direction: column;
  gap: 12px;

  padding: 10px 10px;
}

.logo {
  display: flex;
  flex-direction: row;
  gap: 12px;
}

.brand {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;

  color: var(--green-kelp);
  font-family: var(--playfair-display), 'Playfair Display', serif;
  font-size: 86px;
  font-style: normal;
  font-weight: 900;
  line-height: 80px;
  letter-spacing: -3px;
}
.brand i{
  color: var(--marigold);
}

.description-short,
.tagline{
  display: flex;
  flex-direction: row;
  gap: 9px;
  align-items: center;

  color: var(--marigold);
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 3px;
  text-transform: uppercase;
}

.tagline-dots{
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
}
.dot {
  width: 4px;
  height: 4px;
  border-radius: 2px;
  opacity: 0.7;
  background: var(--marigold);
}
.divider {
  width: 28px;
  height: 1px;
  background: var(--marigold);
  opacity: 0.7;
}

</style>