import {defineStore} from "pinia";
import {useStorage} from '@vueuse/core'


export const useUserStore = defineStore("user", {
    state: () => ({
        user: null,
        token: useStorage('auth_token', '')
    }),
    getters: {
        isLoggedIn(state) {
            return state.token && state.user
        },

    },

    actions: {
        setUser(user, token) {
            console.log("Setting user and token", user, token);
            this.user = user;
            if (token) {
                this.token = token;
            }
        },
        clearUser() {
            this.user = null;
            this.token = null;
        }

    },
});
