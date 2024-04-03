<template>
  <div class="alert alert-dismissible fade show" role="alert"
       :class="{'alert-warning': messagingStore.isError, 'alert-success': !messagingStore.isError}"
       v-if="messagingStore.hasMessage">
    <span>{{ messagingStore.message }}</span>
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>


  </div>
<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
  <div class="toast-header">
    <img src="..." class="rounded me-2" alt="...">
    <strong class="me-auto">Bootstrap</strong>
    <small>11 mins ago</small>
    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
  </div>
  <div class="toast-body">
    Hello, world! This is a toast message.
  </div>
</div>
  <div class="d-flex justify-content-center" v-if="messagingStore.loaderActive">
  <div class="spinner-border" role="status">
    <span class="visually-hidden">Loading...</span>
  </div>
</div>
</template>

<script setup>
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import {useMessagingStore} from "@/stores/messaging";

const messagingStore = useMessagingStore();

</script>
