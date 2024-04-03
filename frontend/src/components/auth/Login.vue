<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">Login</div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="username" class="form-label">Email</label>
                <input type="email" class="form-control" id="username" v-model="username" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
              <router-link to="/register" class="btn btn-link">Register</router-link>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {login as authLogin} from '@/services/auth.js';
import {goToHome} from "@/router";
import {onBeforeRouteLeave} from 'vue-router'
import {useUserStore} from "@/stores/user.js";

let username = useUserStore().last_username;
// TODO Unhardcode passwword
let password = 'password';

function login() {
  return authLogin(username, password).then((e) => {
    return goToHome();
  });
}

onBeforeRouteLeave(() => {
  useUserStore().last_username = username;
})

</script>
