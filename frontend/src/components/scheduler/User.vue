<template>
  <div class="container mt-5">
    <h2>User Details</h2>
    <div><strong>Name:</strong> {{user.name }}</div>
    <div><strong>Email:</strong> {{user.email }}</div>
    <div>
      <span class="badge text-bg-warning" v-if="user.is_scheduler">Scheduler</span>
      <span class="badge text-bg-info" v-if="user.is_employee">Employee</span>
    </div>
    <hr>
    <h2>Shifts</h2>
    <ul class="list-group">
      <li v-for="shift in shifts" :key="shift.id"
                  class="list-group-item d-flex align-items-start list-group-item-action">
        <div class="ms-2 me-auto">
          <div class="fw-bold">{{ shift.id }}</div>
          {{ shift }}
        </div>
      </li>
    </ul>



  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import {getUser} from "@/services/users.js";
import {getShifts} from "@/services/shifts.js";
const route = useRoute();
const props = defineProps(['user']);
const user = ref({});
const shifts = ref([]);

console.log("PROPS", props, window.r = route);
getUser(route.params.userId).then((result) => {
  user.value = result;
  console.log(result);
});

getShifts(route.params.userId).then((result) => {
  shifts.value = result;
  console.log(result);
});

</script>
