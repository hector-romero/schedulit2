<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">Login</div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" v-model="username" required>
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {login as authLogin} from '@/services/auth.js';
import {goToHome} from "@/router";

export default {
  data() {
    return {
      username: 'hector22x@gmail.com',
      password: 'password'
    };
  },

  methods: {
    login() {
      console.log(window.us = this.userStore);
      return authLogin(this.username, this.password).then((e) => {
        return goToHome();
      });
    }
  }
};
</script>
