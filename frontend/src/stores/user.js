import {defineStore} from "pinia";
import {useStorage} from '@vueuse/core'


export const useUserStore = defineStore("user", {
    state: () => ({
        user: null,
        token: useStorage('auth_token', null),
        last_username: useStorage('last_username', null),
    }),
    getters: {
        isLoggedIn(state) {
            return state.token && state.user;
        },

        isEmployee(state) {
            return state.isLoggedIn && state.user.is_employee;
        },

        isScheduler(state) {
            return state.isLoggedIn && state.user.is_scheduler;
        },

        userName(state) {
            if (state.user) {
                return state.user.name || state.user.email;
            }
            return null;
        }

    },

    actions: {
        setUser(user, token) {
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
