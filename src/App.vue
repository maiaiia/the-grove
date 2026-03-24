<script setup>

import AddPlantModal from "@/components/AddPlantModal.vue";
import EditPlantModal from "@/components/EditPlantModal.vue";
import DeletePlantModal from "@/components/DeletePlantModal.vue";
</script>

<template>
  <router-view />
  <AddPlantModal />
  <EditPlantModal />
  <DeletePlantModal />
</template>
<style scoped>

</style>