import {createWebHistory, createRouter} from 'vue-router'

import LoginView from '@/components/auth/Login.vue'
import RegisterView from '@/components/auth/Register.vue'
import UserView from '@/components/scheduler/User.vue';
import {useUserStore} from "@/stores/user.js";

const LOGIN_PATH = '/login';
const HOME_PATH = '/';

const routes = [
    {path: HOME_PATH, component: () => {
        if (useUserStore().isScheduler) {
            return import('@/components/scheduler/Users.vue')
        }
        return import('@/components/Home.vue')
    }},
    {path: '/user/:userId', name: 'UserDetails', component: UserView, props: true},
    {path: LOGIN_PATH, component: LoginView, meta: {requiresNoLoggedIn: true}},
    {path: '/register', component: RegisterView, meta: {requiresNoLoggedIn: true}},
    {path: '/:pathMatch(.*)*', redirect: HOME_PATH}
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to) => {
    // Redirects to login page if needed when trying to access a page that is only for logged users
    // and redirects to home page, if needed, when the page is for non logged users
    const userStore = useUserStore();
    const requiresNoLoggedIn = to.matched.some(x => x.meta.requiresNoLoggedIn);

    if (requiresNoLoggedIn && userStore.isLoggedIn) {
        return HOME_PATH;
    } else if (!requiresNoLoggedIn && !userStore.isLoggedIn) {
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
