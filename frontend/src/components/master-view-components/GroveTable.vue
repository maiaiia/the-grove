<script setup>
import router from "@/router/index.js"
import {useDeletePlantModal} from "@/composables/useDeletePlantModal.js"
import {ref} from "vue"
import {useInfiniteScroll} from "@/composables/useInfiniteScroll.js"

const props = defineProps({ plants: Array })
const emit = defineEmits(['select', 'load-more'])
const tableContainer = ref(null)
const { open: openDeleteModal } = useDeletePlantModal()

const goToPlant = (plant) => router.push(`/plant/${plant.id}`)
const handleDelete = (plant) => {
  openDeleteModal(plant)
}

const { isFetching, hasMore } = useInfiniteScroll(async () => {
  return emit('load-more')
}, {
  target: tableContainer,
  threshold: 150
})
</script>

<template>
  <div class="table-container" ref="tableContainer">
    <table class="grove-table">
      <thead>
      <tr>
        <th>PLANT</th>
        <th>CATEGORY</th>
        <th>AGE</th>
        <th>LAST WATERED</th>
        <th>ACTIONS</th>
      </tr>
      </thead>
      <TransitionGroup name="table-row" tag="tbody" appear>
        <tr
            v-for="(plant, index) in plants"
            :key="plant.id"
            @click="goToPlant(plant)"
            :style="{ '--row-index': index }"
        >
          <td class="cell-plant">
            <img v-if="plant.image" :src="plant.image" :alt="plant.name" class="mini-thumb" />
            <div v-else class="mini-thumb">
              <img src="/grovelogo.svg" alt="grove logo" class="plant-card__placeholder-logo" />
            </div>
            <div>
              <p class="name">{{ plant.name }}</p>
              <p class="latin">{{ plant.latinName }}</p>
            </div>
          </td>
          <td><span class="tag">{{ plant.category }}</span></td>
          <td>
            <div class="age-bar">
              <div class="bar-fill" :style="{ width: (plant.age / 20) * 100 + '%' }"></div>
              <span class="age-label">{{ plant.age }}y</span>
            </div>
          </td>
          <td class="mongoose">{{ plant.lastWatered }}</td>
          <td class="cell-actions">
            <button
                class="delete-btn"
                @click.stop="handleDelete(plant)"
            >
              ✕
            </button>
          </td>
        </tr>
      </TransitionGroup>
    </table>
    <div v-if="isFetching" class="loader">Updating Grove...</div>
    <div v-if="!hasMore && plants.length > 0" class="end-message">End of the garden.</div>
  </div>
</template>

<style scoped>
* {
  font-family: var(--space-mono), monospace;
  color: var(--green-kelp)
}
.table-container { flex: 1; overflow-y: auto; min-height: 0; }
.loader, .end-message {
  padding: 20px;
  text-align: center;
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  color: var(--mongoose);
  text-transform: uppercase;
}
.grove-table { width: 100%; border-collapse: collapse; text-align: left; }
th {
  font-family: var(--space-mono), monospace;
  font-size: 10px;
  color: var(--mongoose);
  padding: 16px;
  border-bottom: 1px solid var(--rodeo-dust);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
tr {
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s;
}
tr:hover { background: #f9f7f2; }
td { padding: 12px 16px; font-family: var(--space-mono), monospace; font-size: 13px; color: var(--green-kelp); }

.mini-thumb, .plant-card__placeholder-logo { width: 45px; height: 45px; object-fit: cover; border-radius: 2px; margin-right: 12px; }
.plant-card__placeholder-logo {
  opacity: 0.7;
}
.cell-plant { display: flex; align-items: center; }
.name {
  font-weight: 800;
  margin: 0;
  font-family: var(--playfair-display), "Playfair Display", serif;
}
.latin {
  font-style: italic;
  font-size: 10px;
  color: var(--mongoose);
  margin: 0;
}
.tag {
  border: 1px solid var(--avocado);
  padding: 4px 8px;
  font-size: 10px;
  border-radius: 3px;
  color: var(--avocado);
  text-transform: uppercase;
}
.age-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 120px;
}
.bar-fill { height: 6px; background: var(--avocado); border-radius: 3px;}
.age-label { font-size: 10px; color: var(--avocado); }

.cell-actions {
  text-align: center;
  padding-right: 24px;
}

.delete-btn {
  background: none;
  border: none;
  color: var(--mongoose);
  font-size: 16px;
  cursor: pointer;
  padding: 8px;
  transition: all ease;
}

.delete-btn:hover {
  color: var(--burnt-umber);
  transform: scale(1.2);
}
</style>