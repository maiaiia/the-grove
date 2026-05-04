<script setup>
defineProps({
  onlineUsers: Array,
  connected: Boolean
})
</script>

<template>
  <div class="chat-sidebar">
    <div class="sidebar-section">
      <h2 class="sidebar-title">The Grove</h2>
      <p class="sidebar-subtitle">Community Chat</p>
    </div>

    <div class="sidebar-divider" />

    <div class="sidebar-section">
      <h3 class="sidebar-label">Online Now</h3>
      <div class="user-list">
        <div
            v-for="user in onlineUsers"
            :key="user"
            class="user-item"
        >
          <span class="user-dot active" />
          <span class="user-name">{{ user }}</span>
        </div>
      </div>
    </div>

    <div class="sidebar-divider" />

    <div class="sidebar-section">
      <h3 class="sidebar-label">Connection</h3>
      <div class="user-item">
        <span class="user-dot" :class="{ active: connected }" />
        <span class="user-name">{{ connected ? 'Connected' : 'Disconnected' }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-sidebar {
  background: var(--green-kelp);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar-title {
  font-family: var(--playfair-display), serif;
  font-size: 20px;
  font-weight: 600;
  color: var(--cream);
  margin: 0;
}

.sidebar-subtitle {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0;
  color: var(--avocado);

}

.sidebar-label {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  letter-spacing: 2px;
  color: var(--avocado);
  text-transform: uppercase;
  margin: 0;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.user-item:hover {
  background: rgba(240, 233, 214, 0.15);
}

.user-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--mongoose);
  flex-shrink: 0;
  transition: background 0.3s ease;
}

.user-dot.active {
  background: var(--marigold);
  box-shadow: 0 0 8px rgba(255, 183, 77, 0.4);
}

.user-name {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  color: var(--cream);
  letter-spacing: 0.3px;
}

.sidebar-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, var(--avocado), transparent);
  margin: 4px 0;
}

@media (max-width: 768px) {
  .chat-sidebar {
    display: none;
  }
}
</style>