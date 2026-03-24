<script setup>
import { useEditPlantModal } from '@/composables/useEditPlantModal'
const { open: openEdit } = useEditPlantModal()
const props = defineProps({ plant: Object })

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-GB', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}
</script>

<template>
  <div class="profile">
    <div class="profile__header">
      <h1 class="profile__name">{{ plant.name }}</h1>
      <p class="profile__latin">{{ plant.latinName.toUpperCase() }}</p>
    </div>

    <div class="profile__section">
      <p class="profile__section-label">Plant Profile</p>
      <div class="profile__grid">
        <div class="profile__field">
          <span class="profile__field-label">Type</span>
          <span class="profile__field-value">{{ plant.category }}</span>
        </div>
        <div class="profile__field">
          <span class="profile__field-label">Age</span>
          <span class="profile__field-value">{{ plant.age }} years</span>
        </div>
        <div class="profile__field">
          <span class="profile__field-label">Date Planted</span>
          <span class="profile__field-value">{{ formatDate(plant.datePlanted) }}</span>
        </div>
        <div class="profile__field">
          <span class="profile__field-label">Photos</span>
          <span class="profile__field-value">{{ plant.photos.length }} entries</span>
        </div>
      </div>
    </div>

    <div class="profile__section">
      <p class="profile__section-label">Care Routine</p>
      <div class="profile__grid">
        <div class="profile__field">
          <span class="profile__field-label">Watering</span>
          <span class="profile__field-value">Every {{ plant.wateringSchedule }} day{{ plant.wateringSchedule === 1 ? '' : 's' }}</span>
        </div>
        <div class="profile__field">
          <span class="profile__field-label">Location</span>
          <span class="profile__field-value">{{ plant.location }}</span>
        </div>
        <div class="profile__field">
          <span class="profile__field-label">Last Watered</span>
          <span class="profile__field-value">{{ formatDate(plant.lastWatered) }}</span>
        </div>
      </div>
    </div>

    <div class="profile__section" >
      <p class="profile__section-label">Notes & History</p>
      <p class="profile__notes" v-if="plant.notes">{{ plant.notes }}</p>
      <p class="profile__notes profile__notes--empty" v-else>No notes recorded for this specimen yet...</p>
    </div>
    <div class="profile__section">

      <a href="#" class="profile__btn profile__btn--outline">Care Details</a>
    </div>
    <div class="profile__actions">
      <button class="profile__btn profile__btn--primary" @click="openEdit(plant)">Edit Plant Details</button>
      <button class="profile__btn profile__btn--danger">Remove from Grove</button>
    </div>
  </div>
</template>

<style scoped>
.profile {
  padding: 10px 64px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.profile::-webkit-scrollbar { width: 3px; }
.profile::-webkit-scrollbar-track { background: transparent; }
.profile::-webkit-scrollbar-thumb { background: var(--rodeo-dust); border-radius: 2px; }

.profile__name {
  font-family: var(--playfair-display), serif;
  font-size: 56px;
  font-weight: 700;
  color: var(--green-kelp);
  line-height: 1.05;
  margin: 0 0 8px;
}

.profile__latin {
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  letter-spacing: 0.15em;
  color: var(--mongoose);
  margin: 0;
}

.profile__section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.profile__section-label {
  font-family: var(--space-mono), monospace;
  font-size: 16px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--avocado);
  margin: 0;
}

.profile__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.profile__field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile__field-label {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--avocado);
}

.profile__field-value {
  font-family: var(--space-mono), "Space Mono", monospace;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: -0.3px;
  color: var(--tree-trunk);
}

.profile__notes {
  font-family: var(--space-mono), monospace;
  font-size: 12px;
  line-height: 1.8;
  color: var(--clay);
  border-left: 2px solid var(--marigold);
  padding-left: 16px;
  margin: 0;
}
.profile__notes--empty {
  opacity: 0.7;
}
.profile__actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid var(--rodeo-dust);
}

.profile__btn {
  width: 100%;
  padding: 16px;
  font-family: var(--space-mono), monospace;
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  text-align: center;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: block;
  border: 1px solid transparent;
}

.profile__section .profile__btn {
  border-radius: 0;
}

.profile__btn--outline {
  background: transparent;
  border-color: var(--marigold);
  color: var(--marigold);
}

.profile__btn--primary {
  background: var(--green-kelp);
  color: var(--parchment);
}

.profile__btn--danger {
  background: transparent;
  color: var(--burnt-umber);
  border-color: var(--burnt-umber);
}

.profile__btn--primary:hover { opacity: 0.85; }
.profile__btn--danger:hover { border-color: var(--burnt-umber); }
</style>