<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center">
      <h1>Users</h1>
      <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addUserModal">Add</button>
    </div>
    <div class="list-group">
      <RouterLink v-for="user in users" :key="user.id"
                  :to="{ name: 'UserDetails', params: { userId: user.id } }"
                  class="list-group-item d-flex align-items-start list-group-item-action">
        <div class="ms-2 me-auto">
          <div class="fw-bold">{{ user.name }}</div>
          {{ user.email }}
        </div>
        <div>
          <span class="badge text-bg-warning" v-if="user.is_scheduler">Scheduler</span>
          <span class="badge text-bg-info" v-if="user.is_employee">Employee</span>
        </div>

      </RouterLink>
    </div>
  </div>

  <div class="modal fade" tabindex="-1" role="dialog" id="addUserModal">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <form @submit.prevent="addNewUser">
          <div class="modal-header">
            <h5 class="modal-title">New User</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">

            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input type="text" class="form-control" id="name" v-model="newUser.name" required>
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input type="email" class="form-control" id="email" v-model="newUser.email" required>
            </div>
            <div class="mb-3">
              <label for="role" class="form-label">Role</label>
              <select class="form-select" id="role" v-model="newUser.role" required>
                <option value="scheduler">Scheduler</option>
                <option value="employee">Employee</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="newUser.password" required>
            </div>
            <div class="mb-3">
              <label for="employeeId" class="form-label">Employee ID (optional)</label>
              <input type="text" class="form-control" id="employeeId" v-model="newUser.employeeId">
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" ref="closeModalButton">
              Close
            </button>
            <button type="submit" class="btn btn-primary">Add User</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
</script>
<script setup>

import {ref} from 'vue';
import {getUsers, addUser} from "@/services/users.js";
import {useMessagingStore} from "@/stores/messaging.js";
import router from "@/router.js";

const newUser = ref({role: 'employee', name: 'some name', email: 'email@email.com', password:'password'});
const closeModalButton = ref(null);

function resetModal() {
  closeModalButton.value.click();
  newUser.value = {role: 'employee'};
}

function addNewUser() {
  const value = newUser.value;
  addUser(value.email, value.password, value.name, value.role, value.employee_id).then(user=> {
    useMessagingStore().setSuccessMessage("Added user");
    resetModal();
    router.push({ name: 'UserDetails', params: { userId: user.id } });
  });
}

let users = ref([]);


getUsers().then((result) => {
  users.value = result;
});


</script>
