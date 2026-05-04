<script setup>
import { ref } from 'vue'

const emit = defineEmits(['send'])
const inputText = ref('')

const send = () => {
  if (!inputText.value.trim()) return
  emit('send', inputText.value.trim())
  inputText.value = ''
}

const handleKey = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}
</script>

<template>
  <div class="chat-input">
    <div class="input-wrapper">
      <input
          class="input-field"
          v-model="inputText"
          @keydown="handleKey"
          placeholder="Share your thoughts..."
          type="text"
      />
      <button
          class="send-button"
          @click="send"
          :disabled="!inputText.trim()"
      >
        <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  padding: 16px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  background: var(--parchment);
  flex-shrink: 0;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
  background: var(--cream);
  border-radius: 24px;
  padding: 8px 12px 8px 20px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

.input-wrapper:focus-within {
  border-color: var(--avocado);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--avocado) 15%, transparent);
}

.input-field {
  flex: 1;
  background: transparent;
  border: none;
  padding: 8px 0;
  font-family: var(--space-mono), monospace;
  font-size: 13px;
  color: var(--green-kelp);
  outline: none;
  letter-spacing: 0.3px;
}

.input-field::placeholder {
  color: var(--mongoose);
  font-style: italic;
}

.send-button {
  background: var(--green-kelp);
  color: var(--parchment);
  border: none;
  padding: 10px 20px;
  border-radius: 18px;
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 70px;
}

.send-button:hover:not(:disabled) {
  background: color-mix(in srgb, var(--green-kelp) 85%, black);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(44, 59, 34, 0.2);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-text {
  text-transform: uppercase;
}

@media (max-width: 768px) {
  .chat-input {
    padding: 12px 16px;
  }

  .input-wrapper {
    padding: 6px 8px 6px 16px;
  }
}
</style>