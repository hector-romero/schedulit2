<template>
  <div class="d-flex justify-content-center loading" v-if="messagingStore.loaderActive">
    <div class="spinner-border spinner" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script>
import 'vue-toast-notification/dist/theme-bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
</script>

<script setup>
import {useMessagingStore} from "@/stores/messaging";
import {useToast} from 'vue-toast-notification';
import {watch} from "vue";

const messagingStore = useMessagingStore();
const toast = useToast();

watch(
    () => messagingStore.message, () => {
      toast.clear();
      let message = messagingStore.message;
      if (!message) {
        return
      } else if (message.detail) {
        message = message.detail;
      }

      if (messagingStore.isError) {
        toast.error(message);
      } else {
        toast.success(message);
      }
    }
);
</script>

<style>

.loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 10000;
  background: rgba(30, 30, 30, .2);
}
.spinner {
  position: absolute;
  top: 50%;
  text-align: center;
}
</style>
