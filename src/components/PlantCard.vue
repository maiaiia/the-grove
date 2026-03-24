<script setup>

</script>

<template>
  <div class="plant-card">
    <div class="image-wrapper">
      <img :src="image" :alt="name"/>
    </div>
    <div class="content">
      <h3 class="name">{{name}}</h3>
      <p class="latin">{{latinName}}</p>
      <span class="age">{{age}}</span>
    </div>
  </div>
</template>

<style scoped>

</style>