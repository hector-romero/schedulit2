<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">Register</div>
          <div class="card-body">
            <form @submit.prevent="register">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="name" required>
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required>
              </div>
              <div class="mb-3">
                <label for="role" class="form-label">Role</label>
                <select class="form-select" id="role" v-model="role" required>
                  <option value="">Select Role</option>
                  <option value="scheduler">Scheduler</option>
                  <option value="employee">Employee</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
              <div class="mb-3">
                <label for="passwordConfirmation" class="form-label">Confirm Password</label>
                <input type="password" class="form-control" id="passwordConfirmation" v-model="passwordConfirmation"
                       required>
              </div>
              <div class="mb-3">
                <label for="employeeId" class="form-label">Employee ID (optional)</label>
                <input type="text" class="form-control" id="employeeId" v-model="employeeId">
              </div>
              <button type="submit" class="btn btn-primary">Register</button>
              <router-link to="/login" class="btn btn-link">Back to Login</router-link>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {onBeforeRouteLeave} from 'vue-router'
import {goToHome} from "@/router.js";
import {register as authRegister} from "@/services/auth.js";
import {useMessagingStore} from "@/stores/messaging.js";
import {useUserStore} from "@/stores/user.js";

let name = 'Hector',
    email = useUserStore().last_username,
    role = 'employee',
    password = 'password',
    passwordConfirmation = 'password',
    employeeId = '';

function register() {
  if (password !== passwordConfirmation) {
    useMessagingStore().setErrorMessage('Passwords do not match!');
    return;
  }
  authRegister(email, password, name, role, employeeId).then(() => {
    return goToHome();
  })

}

onBeforeRouteLeave(() => {
  useUserStore().last_username = email;
})


</script>
