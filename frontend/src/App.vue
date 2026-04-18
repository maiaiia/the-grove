<script setup>

import AddPlantModal from "@/components/modals/AddPlantModal.vue";
import EditPlantModal from "@/components/modals/EditPlantModal.vue";
import DeletePlantModal from "@/components/modals/DeletePlantModal.vue";
</script>

<template>
  <router-view />
  <AddPlantModal />
  <EditPlantModal />
  <DeletePlantModal />
</template>
<style scoped>

</style>