import http from "@/services/api";
import {useUserStore} from "@/stores/user.js";

export async function checkLogin() {
    console.log("CHECKING LOGIN");
    const userStore = useUserStore();
    if (! userStore.token) {
        console.log("CHECKED LOGIN");
        return Promise.resolve();
    }
    return http.get('account/').then((response) => {
        console.log("CHECKED LOGI2N");
        userStore.setUser(response.user, response.token);
        return response.user;
    }).catch(() => {
        console.log("CHECKED LOGIN3");
        userStore.clearUser();
        return Promise.resolve();
    });
}
export async function login (username, password) {
    return http.post('account/login/', {username, password}).then((response) => {
        console.log("RESPONSE", window.r = response);
        useUserStore().setUser(response.user, response.token);
        return response.user
    });
}

export async function logout() {
    return http.post('account/logout/').then(()=> {
        useUserStore().clearUser();
    });
}
