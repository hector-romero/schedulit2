import { createMemoryHistory, createRouter } from 'vue-router'

import HomeView from './components/Home.vue'
import LoginView from './components/Login.vue'
import {useUserStore} from "@/stores/user.js";

const LOGIN_PATH = '/login';
const HOME_PATH = '/';
const routes = [
  { path: HOME_PATH, component: HomeView },
  { path: LOGIN_PATH, component: LoginView, meta: {requiresNoLoggedIn: true}},
];

const router = createRouter({
  history: createMemoryHistory(),
  routes,
});


router.beforeEach(async (to) => {
    // Redirects to login page if needed when trying to access a page that is only for logged users
    // and redirects to home page, if needed, when the page is for non logged users
    const userStore = useUserStore();
    const requiresNoLoggedIn = to.matched.some(x=> x.meta.requiresNoLoggedIn);

    console.log("HERE ROUTER", to.path, userStore.isLoggedIn, requiresNoLoggedIn);
    if (requiresNoLoggedIn && userStore.isLoggedIn) {
        return HOME_PATH;
    } else if (!requiresNoLoggedIn && !userStore.isLoggedIn) {
        // auth.returnUrl = to.fullPath;
        return LOGIN_PATH;
    }
});

export function goToLogin() {
    return router.push(LOGIN_PATH);
}

export function goToHome() {
    return router.push(HOME_PATH);
}


export default router;
