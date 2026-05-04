<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useChatStore } from '@/stores/chatStore.js'
import AppNav from "@/components/AppNav.vue"
import ChatSidebar from "@/components/chat-components/ChatSidebar.vue"
import ChatMessages from "@/components/chat-components/ChatMessages.vue"
import ChatInput from "@/components/chat-components/ChatInput.vue"

const chatStore = useChatStore()
const inputText = ref('')

const handleSend = (message) => {
  chatStore.send(message)
}

onMounted(async () => {
  await chatStore.init()
})

onUnmounted(() => {
  chatStore.disconnect()
})
</script>

<template>
  <div class="chat-view">
    <AppNav />
    <div class="chat-view__body">
      <ChatSidebar
          :online-users="chatStore.onlineUsers"
          :connected="chatStore.connected"
      />

      <div class="chat-main">
        <div class="chat-header">
          <h1 class="chat-header__title">Global Chat</h1>
          <span class="chat-header__count">{{ chatStore.onlineUsers.length }} online</span>
        </div>

        <ChatMessages :messages="chatStore.messages" />

        <ChatInput @send="handleSend" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--cream);
  overflow: hidden;
}

.chat-view__body {
  flex: 1;
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 24px;
  padding: 24px 48px;
  min-height: 0;
}

.chat-main {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  min-height: 0;
  background: var(--parchment);
}

.chat-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--avocado);
  background: var(--parchment);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.chat-header__title {
  font-family: var(--playfair-display), serif;
  font-size: 24px;
  font-weight: 600;
  color: var(--green-kelp);
  margin: 0;
}

.chat-header__count {
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  color: var(--avocado);
  letter-spacing: 0.5px;
}

@media (max-width: 768px) {
  .chat-view__body {
    grid-template-columns: 1fr;
    padding: 16px;
    gap: 16px;
  }
}
</style>