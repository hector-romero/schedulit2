import http from "@/services/api";
import {useUserStore} from "@/stores/user.js";

export async function checkLogin() {
    const userStore = useUserStore();
    if (!userStore.token) {
        return Promise.resolve();
    }
    return http.get('account/').then((response) => {
        userStore.setUser(response.user, response.token);
        return response.user;
    }).catch(() => {
        userStore.clearUser();
        return Promise.resolve();
    });
}

export async function login(username, password) {
    return http.post('account/login/', {username, password}).then((response) => {
        useUserStore().setUser(response.user, response.token);
        return response.user
    });
}

export async function logout() {
    return http.post('account/logout/').then(() => {
        useUserStore().clearUser();
    });
}

export async function register(email, password, name, role, employee_id) {
    return http.post('account/register/', {email, password, name, role, employee_id}).then((response) => {
        useUserStore().setUser(response.user, response.token);
        return response.user;
    });
}
