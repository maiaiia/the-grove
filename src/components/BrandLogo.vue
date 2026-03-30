<script setup>
import {computed, useCssVars} from "vue";

const props = defineProps({
  theme: {type: String, default: 'light' }
})
const brandColor = computed(() => props.theme === 'dark' ? 'var(--cream)' : 'var(--green-kelp)');
</script>

<template>
  <div class="brand-logo">
    <div class="eyebrow">
      <div class="divider" />
      <p>A living plant journal</p>
    </div>

    <div class="logo">
      <img
          :src="theme === 'dark' ? '/src/assets/grovelogo.svg' : '/src/assets/logo-transparent.svg'"
          alt="logo"
      />
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
      <p>Every leaf, a new season</p>
    </div>
  </div>
</template>

<style scoped>
.brand-logo {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.eyebrow,
.tagline {
  display: flex;
  flex-direction: row;
  gap: 9px;
  align-items: center;
  color: var(--marigold);
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  letter-spacing: 3px;
  text-transform: uppercase;
}

.divider {
  width: 28px;
  height: 1px;
  background: var(--marigold);
  opacity: 0.7;
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
  font-family: var(--playfair-display), serif;
  font-size: 86px;
  font-weight: 900;
  line-height: 80px;
  letter-spacing: -3px;

  color: v-bind(brandColor);
}

.brand i { color: var(--marigold); }

.tagline-dots {
  display: flex;
  gap: 4px;
}

.dot {
  width: 4px;
  height: 4px;
  border-radius: 2px;
  opacity: 0.7;
  background: var(--marigold);
}
@media (max-width: 768px) {
  .logo img {
    height: 30vw;
  }

  .brand {
    font-size: 42px;
    line-height: 38px;
    letter-spacing: -1px;
  }

  .eyebrow, .tagline {
    letter-spacing: 1px;
    font-size: 8px;
  }

  .divider {
    width: 15px;
  }

  .logo {
    gap: 10px;
    align-items: center;
  }

  .brand-logo {
    gap: 8px;
  }
}
</style>