<script setup>
import {reactive, ref} from 'vue'
import { useAddPlantModal } from '@/composables/useAddPlantModal.js'
import { usePlantStore } from '@/stores/plantStore.js'
import { createPlant } from '@/data/plants.js'
import { PLANT_CATEGORIES, PLANT_LOCATIONS } from '@/data/plantCategories.js'

const { isOpen, close } = useAddPlantModal()
const store = usePlantStore()

const empty = () => ({
  name: '',
  latinName: '',
  category: '',
  datePlanted: '',
  wateringSchedule: '',
  location: '',
})

const form = reactive(empty())
const errors = reactive({})

function validate() {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!form.name) errors.name = 'Required'
  if (!form.latinName) errors.latinName = 'Required'
  if (!form.category) errors.category = 'Required'
  if (!form.datePlanted) errors.datePlanted = 'Required'
  if (!form.wateringSchedule || form.wateringSchedule < 1) errors.wateringSchedule = 'Must be at least 1'
  if (!form.location) errors.location = 'Required'
  return Object.keys(errors).length === 0
}
const serverError = ref(null)
async function submit() {
  if (!validate()) return
  try {
    await store.addPlant(createPlant({
      id: 0,
      name: form.name,
      latinName: form.latinName,
      category: form.category,
      datePlanted: form.datePlanted,
      wateringSchedule: Number(form.wateringSchedule),
      location: form.location,
      lastWatered: form.datePlanted,
      photos: [],
      notes: '',
    }))
    Object.assign(form, empty())
    serverError.value=null;
    close()
  } catch (error) {
    serverError.value = error.response?.data?.message || "The Grove is currently unreachable."
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
              <p class="modal__eyebrow">Add to your collection</p>
              <h2 class="modal__title">New <em>Plant</em></h2>
            </div>
            <button class="modal__close" @click="close">✕</button>
          </div>

          <div class="modal__body">
            <!-- Name + Latin -->
            <div class="modal__row">
              <div class="modal__field" :class="{ error: errors.name }">
                <label class="modal__label">Plant Name</label>
                <input v-model="form.name" class="modal__input" placeholder="e.g. Monstera Rex" />
                <span class="modal__error" v-if="errors.name">{{ errors.name }}</span>
              </div>
              <div class="modal__field" :class="{ error: errors.latinName }">
                <label class="modal__label">Latin Name</label>
                <input v-model="form.latinName" class="modal__input" placeholder="e.g. Monstera deliciosa" />
                <span class="modal__error" v-if="errors.latinName">{{ errors.latinName }}</span>
              </div>
            </div>

            <!-- Category + Location -->
            <div class="modal__row">
              <div class="modal__field" :class="{ error: errors.category }">
                <label class="modal__label">Category</label>
                <select v-model="form.category" class="modal__input modal__select">
                  <option value="" disabled>Select category</option>
                  <option v-for="cat in Object.values(PLANT_CATEGORIES)" :key="cat" :value="cat">{{ cat }}</option>
                </select>
                <span class="modal__error" v-if="errors.category">{{ errors.category }}</span>
              </div>
              <div class="modal__field" :class="{ error: errors.location }">
                <label class="modal__label">Location</label>
                <select v-model="form.location" class="modal__input modal__select">
                  <option value="" disabled>Select location</option>
                  <option v-for="loc in Object.values(PLANT_LOCATIONS)" :key="loc" :value="loc">{{ loc }}</option>
                </select>
                <span class="modal__error" v-if="errors.location">{{ errors.location }}</span>
              </div>
            </div>

            <!-- Date + Watering -->
            <div class="modal__row">
              <div class="modal__field" :class="{ error: errors.datePlanted }">
                <label class="modal__label">Date Planted</label>
                <input v-model="form.datePlanted" type="date" class="modal__input" />
                <span class="modal__error" v-if="errors.datePlanted">{{ errors.datePlanted }}</span>
              </div>
              <div class="modal__field" :class="{ error: errors.wateringSchedule }">
                <label class="modal__label">Water Every (days)</label>
                <input v-model="form.wateringSchedule" type="number" min="1" class="modal__input" placeholder="e.g. 7" />
                <span class="modal__error" v-if="errors.wateringSchedule">{{ errors.wateringSchedule }}</span>
              </div>
            </div>
          </div>

          <div class="modal__footer">
            <button class="modal__btn modal__btn--ghost" @click="close">Cancel</button>
            <button class="modal__btn modal__btn--primary" @click="submit">Add to Grove</button>
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