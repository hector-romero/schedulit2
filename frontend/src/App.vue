<template>
  <div>
    <!-- Bootstrap Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link to="/" class="navbar-brand">Schedulit</router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item" v-if="!userStore.user">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item" v-if="userStore.user">
              <button @click="logout" class="btn btn-link nav-link">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <Alert></Alert>
    <!-- Main Content Area -->
    <router-view ></router-view>

  </div>
</template>

<script>
import {useUserStore} from "@/stores/user";
import {logout} from "@/services/auth";
import {goToLogin} from "@/router";
import Alert from "@/components/Alert.vue";

export default {
  components: {Alert},
  setup() {
    const userStore = useUserStore();
    return {userStore};
  },

  methods: {
    logout() {
      logout().then(() => {
        return goToLogin();
      });
    }
  }
};
</script>

<style>
/* Add custom styles here */
</style>
