<template>
  <header class="splash-navbar">

    <nav class="nav-links">
      <a href="/grove" class="link">About</a>
      <a href="#" class="link">Community</a>
      <a href="/sign-in" class="link">Sign In</a>
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