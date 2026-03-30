<script setup>
import router from "@/router/index.js";

defineProps({ plants: Array })
const emit = defineEmits(['select'])

const goToPlant = (plant) => router.push(`/plant/${plant.id}`)
</script>

<template>
  <div class="table-container">
    <table class="grove-table">
      <thead>
      <tr>
        <th>PLANT</th>
        <th>CATEGORY</th>
        <th>AGE</th>
        <th>WATERING</th>
        <th>LOCATION</th>
        <th>PHOTOS</th>
        <th>LAST WATERED</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="plant in plants" :key="plant.id" @click="goToPlant(plant)">
        <td class="cell-plant">
          <img :src="plant.image" class="mini-thumb" />
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
        <td>{{ plant.wateringSchedule }}</td>
        <td>{{ plant.location }}</td>
        <td class="bold">{{ plant.photos?.length || 0 }}</td>
        <td class="mongoose">{{ plant.lastWatered }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
* {
  font-family: var(--space-mono), monospace;
  color: var(--green-kelp)
}
.table-container { flex: 1; overflow-y: auto; }
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
tr { border-bottom: 1px solid #eee; cursor: pointer; transition: background 0.2s; }
tr:hover { background: #f9f7f2; }
td { padding: 12px 16px; font-family: var(--space-mono), monospace; font-size: 13px; color: var(--green-kelp); }
.mini-thumb { width: 45px; height: 45px; object-fit: cover; border-radius: 2px; margin-right: 12px; }
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
</style>