import {defineStore} from "pinia";
import {useStorage} from '@vueuse/core'


export const useMessagingStore = defineStore("messaging", {
    state: () => ({
        loaderActive: null,
        message: null,
        isError: false
    }),
    getters: {
        hasMessage: (state) => {
            return !!state.message
        }
    },
    actions: {
        activateLoader() {
            this.loaderActive = true;
        },
        deactivateLoader() {
            this.loaderActive = false;
        },
        setMessage(message, isError) {
            this.message = message;
            this.isError = isError;
        },
        setSuccessMessage(message) {
            this.setMessage(message, false);
        },

        setErrorMessage(message) {
            this.setMessage(message, true);
        }
    },
});
