<template>
  <Navbar></Navbar>
  <Alert></Alert>
  <!-- Main Content Area -->
  <router-view></router-view>
</template>

<script setup>
import Alert from "@/components/Alert.vue";
import Navbar from "@/components/Navbar.vue";

</script>
