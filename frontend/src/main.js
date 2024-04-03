import './assets/main.scss'
import 'bootstrap/dist/css/bootstrap.min.css';

import { createApp } from 'vue'
import { createPinia } from "pinia";

import App from './App.vue'
import router from './router';
import {checkLogin} from "@/services/auth";

const pinia = createPinia();

const app = createApp(App).use(pinia);

await checkLogin();

import {useMessagingStore} from "@/stores/messaging.js";

window.messagingStore = useMessagingStore();
app.use(router).mount('#app');
