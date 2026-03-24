<template>
  <header class="navbar">
    <!-- Left: Logo -->
    <div class="logo">
      <img src="/src/assets/grovelogo.svg" width="46px" height="46px">
      <span class="brand"><a href = "/">The Grove</a></span>
    </div>

    <!-- Right: Navigation -->
    <nav class="nav-links">
      <a href="/grove" class="link">My Grove</a>
      <a href="/statistics" class="link">Statistics</a>

      <button class="add-btn" @click="open">+ Add Plant</button>
    </nav>
  </header>
</template>

<script setup>
  import { useAddPlantModal } from '@/composables/useAddPlantModal'
  const { open } = useAddPlantModal()
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 10px 48px;
  border-bottom: 1px solid var(--rodeo-dust);
}

/* Left side */
.logo {
  display: flex;
  align-items: center;
  gap: 10px;

}

.icon {
  display: flex;
  align-items: center;
  width: 46px;
  height: 46px;
}

.brand,
.brand a{
  color: var(--green-kelp);
  font-family: var(--playfair-display), "Playfair Display", serif;
  font-size: 18px;
  font-weight: 900;
  line-height: normal;
  letter-spacing: -0.5px;
}

.brand a{
  text-decoration: none;
}

/* Right side */
.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;

  font-family: 'Space Mono', monospace;
}

.link {
  text-decoration: none;
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--avocado);
  text-transform: uppercase;
}

.link:hover {
  color: #2f4f3f;
}

/* Button */
.add-btn {
  background: var(--green-kelp);
  color: var(--cream);
  text-align: center;
  border: none;
  padding: 8px 16px;
  text-transform: uppercase;
  cursor: pointer;

  font-family: 'Space Mono', monospace;
  font-size: 10px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1px;
}

.add-btn:hover {
  opacity: 0.9;
}
</style>