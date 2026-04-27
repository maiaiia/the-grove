<script setup>
import { reactive, ref } from 'vue'
import { useAddPhotoModal } from '@/composables/useAddPhotoModal.js'
import { usePlantStore } from '@/stores/plantStore.js'

const props = defineProps({ plantId: Number })
const { isOpen, close } = useAddPhotoModal()
const store = usePlantStore()

const empty = () => ({
  url: '',
  caption: '',
})

const form = reactive(empty())
const serverError = ref(null)

async function submit() {
  if (!form.url) return // Simple check: must have a filename

  try {
    await store.uploadPhoto(props.plantId, {
      url: form.url,
      caption: form.caption
    })
    Object.assign(form, empty())
    serverError.value = null
    close()
  } catch (error) {
    serverError.value = "Failed to link the photo to the Grove."
  }
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

          <Transition name="fade">
            <div v-if="serverError" class="modal__alert">
              <p>{{ serverError }}</p>
            </div>
          </Transition>

          <div class="modal__header">
            <div>
              <p class="modal__eyebrow">Document Growth</p>
              <h2 class="modal__title">Add <em>Memory</em></h2>
            </div>
            <button class="modal__close" @click="close">✕</button>
          </div>

          <div class="modal__body">
            <div class="modal__field">
              <label class="modal__label">Filename</label>
              <input v-model="form.url" class="modal__input" placeholder="e.g. monstera_spring.jpg" />
            </div>

            <div class="modal__field">
              <label class="modal__label">Caption</label>
              <input v-model="form.caption" class="modal__input" placeholder="Describe the progress..." />
            </div>
          </div>

          <div class="modal__footer">
            <button class="modal__btn modal__btn--ghost" @click="close">Cancel</button>
            <button class="modal__btn modal__btn--primary" @click="submit">Link Photo</button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/*TODO this is  DRY*/
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
  max-width: 580px;
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
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--marigold);
  margin: 0 0 6px;
}

.modal__title {
  font-family: var(--playfair-display), serif;
  font-size: 32px;
  font-weight: 700;
  color: var(--green-kelp);
  margin: 0;
  line-height: 1;
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
  padding: 4px;
  line-height: 1;
}

.modal__close:hover { color: var(--green-kelp); }

.modal__body {
  padding: 28px 36px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.modal__field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.modal__label {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--mongoose);
}

.modal__input {
  background: var(--cream);
  border: 1px solid rgba(44, 59, 34, 0.15);
  border-radius: 4px;
  padding: 10px 12px;
  font-family: var(--playfair-display), serif;
  font-size: 15px;
  color: var(--green-kelp);
  outline: none;
  transition: border-color 0.2s;
}

.modal__input:focus { border-color: var(--marigold); }
.modal__select { cursor: pointer; }

.modal__field.error .modal__input { border-color: #c0392b; }

.modal__error {
  font-family: var(--space-mono), monospace;
  font-size: 9px;
  color: #c0392b;
  letter-spacing: 0.05em;
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
  background: transparent;
  border-color: var(--rodeo-dust);
  color: var(--mongoose);
}

.modal__btn--primary {
  background: var(--green-kelp);
  color: var(--parchment);
}

.modal__btn--ghost:hover { border-color: var(--green-kelp); color: var(--green-kelp); }
.modal__btn--primary:hover { opacity: 0.85; }

/* Transition */
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: transform 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal, .modal-leave-to .modal { transform: translateY(12px); }

.modal__alert {
  border-left: 3px solid #c0392b;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  border-radius: 4px;
}

.modal__alert p {
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  color: #c0392b;
  margin: 0;
}
</style>