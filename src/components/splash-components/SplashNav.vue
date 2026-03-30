<template>
  <header class="splash-navbar">

    <nav class="nav-links">
      <router-link to="/grove" class="link">About</router-link>
      <router-link to="#" class="link">Community</router-link>
      <router-link to="/sign-in" class="link">Sign In</router-link>
    </nav>
  </header>
</template>

<script setup>

</script>

<style scoped>
.splash-navbar {
  display: flex;
  justify-content: right;
  align-items: center;

  padding: 20px 48px;
  border-top: 2.5px solid var(--marigold);
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
  color: var(--mongoose);
  text-transform: uppercase;
}

.link:hover {
  color: #2f4f3f;
}
</style>