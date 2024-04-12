<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark ">
    <div class="container-fluid">
      <span class="navbar-brand mb-0 h1" >
        <IconCalendar></IconCalendar>
      </span>
      <router-link to="/" class="navbar-brand mb-0 h1">
        Schedulit
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            {{ backendStore.backend.name }}
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            <li v-for="(backend, backend_key) in backendStore.backends">
              <button class="dropdown-item" @click="backendStore.selectBackend(backend_key)">
                {{backend.name}}
              </button>
            </li>

          </ul>
        </li>
          <li class="nav-item" v-if="!userStore.user">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item" v-if="userStore.user">
            <button @click="logout" class="btn btn-link nav-link">Logout {{ userStore.userName }}</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

</template>

<script setup>
import {useUserStore} from "@/stores/user";
import {logout as authLogout} from "@/services/auth";
import {goToLogin} from "@/router";
import IconCalendar from "@/components/icons/IconCalendar.vue";
import {useBackendStore} from "@/stores/backend.js";

const userStore = useUserStore();
const backendStore = useBackendStore();

function logout() {
  authLogout().then(() => {
    return goToLogin();
  });
}

</script>
