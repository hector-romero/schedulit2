<template>
  <h3>HELLO! {{ userStore.userName }}</h3>
</template>

<script setup>
import {useUserStore} from "@/stores/user.js";
const userStore = useUserStore();

</script>
