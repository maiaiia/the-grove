<script setup>
const props = defineProps({
  message: Object,
  isMine: Boolean
})

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div
      v-if="message.type === 'system'"
      class="message message--system"
  >
    <div class="message__system-text">{{ message.text }}</div>
  </div>

  <div
      v-else
      class="message"
      :class="{ 'message--mine': isMine, 'message--other': !isMine }"
  >
    <div class="message__meta">
      <span class="message__username">{{ message.username }}</span>
      <span class="message__time">{{ formatTime(message.timestamp) }}</span>
    </div>
    <div class="message__bubble">
      {{ message.text }}
    </div>
  </div>
</template>

<style scoped>
.message {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 70%;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message--mine {
  align-self: flex-end;
  align-items: flex-end;
}

.message--other {
  align-self: flex-start;
  align-items: flex-start;
}

.message--system {
  align-self: center;
  align-items: center;
  max-width: 100%;
}

.message__meta {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 4px;
}

.message__username {
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  letter-spacing: 0.5px;
  color: var(--avocado);
  font-weight: 600;
}

.message__time {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  color: var(--mongoose);
  letter-spacing: 0.3px;
}

.message__bubble {
  padding: 12px 16px;
  font-family: var(--space-mono), monospace;
  font-size: 13px;
  line-height: 1.6;
  letter-spacing: 0.2px;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.message--mine .message__bubble {
  background: var(--green-kelp);
  color: var(--cream);
  box-shadow: 0 2px 8px rgba(44, 59, 34, 0.15);
}

.message--other .message__bubble {
  background: var(--cream);
  color: var(--green-kelp);
  border: 1px solid var(--avocado);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message__system-text {
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  color: var(--mongoose);
  letter-spacing: 0.5px;
  text-align: center;
  padding: 8px 16px;
  background: color-mix(in srgb, var(--avocado) 10%, transparent);
  border-radius: 16px;
  font-style: italic;
}

@media (max-width: 768px) {
  .message {
    max-width: 85%;
  }
}
</style>