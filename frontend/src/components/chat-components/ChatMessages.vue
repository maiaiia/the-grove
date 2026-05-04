<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import { useAuthStore } from '@/stores/authstore.js'
import ChatMessage from './ChatMessage.vue'

const props = defineProps({
  messages: Array
})

const authStore = useAuthStore()
const messagesEl = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight
    }
  })
}

watch(() => props.messages.length, scrollToBottom)
</script>

<template>
  <div class="chat-messages" ref="messagesEl">
    <div class="messages-inner">
      <TransitionGroup name="message" appear>
        <ChatMessage
            v-for="msg in messages"
            :key="msg.id || msg.timestamp"
            :message="msg"
            :is-mine="msg.username === authStore.username"
        />
      </TransitionGroup>
    </div>
  </div>
</template>

<style scoped>
.chat-messages {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.messages-inner {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 100%;
}

/* Message transitions */
.message-enter-active {
  transition: all 0.3s ease;
}

.message-leave-active {
  transition: all 0.2s ease;
}

.message-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.message-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.message-move {
  transition: transform 0.3s ease;
}
</style>