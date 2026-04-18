<script setup>
import { useRoute } from 'vue-router'
import { usePlantStore } from '@/stores/plantStore.js'
import {computed, onMounted, ref} from 'vue'
import AppNav from '@/components/AppNav.vue'
import DetailBreadcrumb from '@/components/detail-view-components/DetailBreadcrumb.vue'
import PlantTimeline from '@/components/detail-view-components/PlantTimeline.vue'
import PlantProfile from '@/components/detail-view-components/PlantProfile.vue'

const route = useRoute()
const store = usePlantStore()

const plant = computed(() => store.currentPlant)

onMounted(() => {
  store.fetchPlantById(route.params.id)
})

const activeTab = ref('profile') //or 'timeline'
</script>

<template>
  <div class="detail" v-if="plant">
    <AppNav />
    <DetailBreadcrumb :plant-name="plant.name" />
    <div class="mobile-tabs">
      <button
          :class="{ active: activeTab === 'profile' }"
          @click="activeTab = 'profile'"
      >
        Profile
      </button>
      <button
          :class="{ active: activeTab === 'timeline' }"
          @click="activeTab = 'timeline'"
      >
        Timeline
      </button>
    </div>
    <div class="detail__body">
      <PlantTimeline
          class="timeline-tab"
          :plant="plant"
      />
      <PlantProfile
          class="profile-tab"
          :plant="plant"
      />
    </div>
  </div>
</template>

<style scoped>
.detail {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-background);
  overflow: hidden;
}

.detail__body {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 0;
}
.mobile-tabs {
  display: none;
}
.timeline-tab,
.profile-tab {
  display: flex;
}
@media (max-width: 768px) {
  .mobile-tabs {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 20px 24px;
    border: 1px solid var(--rodeo-dust);
  }

  .mobile-tabs button {
    flex: 1;
    padding: 12px;
    background: var(--parchment);
    border: none;
    font-family: var(--space-mono), monospace;
    font-size: 12px;
    text-transform: uppercase;
    color: var(--mongoose);
    cursor: pointer;
  }

  .mobile-tabs button.active {
    background: var(--green-kelp);
    color: var(--parchment);
  }

  .detail__body {
    grid-template-columns: 1fr;
    display: flex;
    overflow-y: auto;
  }

  .timeline-tab,
  .profile-tab {
    display: none;
  }

  .timeline-tab {
    display: v-bind(activeTab === 'timeline' ? 'flex' : 'none');
  }

  .profile-tab {
    display: v-bind(activeTab === 'profile' ? 'flex' : 'none');
  }
}
</style>