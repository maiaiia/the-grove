<script setup>
import { useDeletePlantModal } from '@/composables/useDeletePlantModal'
import { usePlantStore } from '@/stores/plantStore'
import { useRouter } from 'vue-router'

const { isOpen, plantToDelete, close } = useDeletePlantModal()
const store = usePlantStore()
const router = useRouter()

function confirm() {
  store.deletePlant(plantToDelete.value.id)
  close()
  router.push('/grove')
}

function handleBackdrop(e) {
  if (e.target === e.currentTarget) close()
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-backdrop" @click="handleBackdrop">
        <div class="modal">

          <div class="modal__header">
            <div>
              <p class="modal__eyebrow">This cannot be undone</p>
              <h2 class="modal__title">Remove <em>{{ plantToDelete?.name }}</em>?</h2>
            </div>
            <button class="modal__close" @click="close">✕</button>
          </div>

          <div class="modal__body">
            <p class="modal__message">
              <em>{{ plantToDelete?.name }}</em> and all of its photos and history
              will be permanently removed from your grove.
            </p>
          </div>

          <div class="modal__footer">
            <button class="modal__btn modal__btn--ghost" @click="close">Keep it</button>
            <button class="modal__btn modal__btn--danger" @click="confirm">Yes, remove it</button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(20, 28, 15, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal {
  background: var(--parchment);
  width: 100%;
  max-width: 440px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.modal__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px 36px 24px;
  border-bottom: 1px solid rgba(44, 59, 34, 0.08);
}
.modal__eyebrow {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #c0392b;
  margin: 0 0 6px;
}
.modal__title {
  font-family: var(--playfair-display), serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--green-kelp);
  margin: 0;
  line-height: 1.2;
}
.modal__title em {
  font-style: italic;
  color: var(--marigold);
}
.modal__close {
  background: none;
  border: none;
  font-size: 14px;
  color: var(--mongoose);
  cursor: pointer;
}
.modal__close:hover { color: var(--green-kelp); }
.modal__body {
  padding: 28px 36px;
}
.modal__message {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  line-height: 1.8;
  color: var(--clay);
  margin: 0;
  border-left: 2px solid var(--burnt-umber);
  padding-left: 16px;
}
.modal__message em {
  font-style: normal;
  color: var(--green-kelp);
  font-weight: 500;
}
.modal__footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 36px 28px;
  border-top: 1px solid rgba(44, 59, 34, 0.08);
}
.modal__btn {
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid transparent;
}
.modal__btn--ghost {
  background: var(--green-kelp);
  color: var(--parchment);
}
.modal__btn--danger {
  background: var(--burnt-umber);
  color: var(--parchment);
}
.modal__btn--ghost:hover,
.modal__btn--danger:hover { opacity: 0.85; }
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: transform 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal, .modal-leave-to .modal { transform: translateY(12px); }
</style>