import {defineStore} from "pinia";
import {useStorage} from '@vueuse/core'

const rails_backend = import.meta.env.VITE_API_URL_RAILS;
const django_backend = import.meta.env.VITE_API_URL_DJANGO;

const backends = {
    'django': {
        'url': django_backend,
        'name': 'Django Backend'
    },
    'rails': {
        'url': rails_backend,
        'name': 'Rails Backend'
    },
};

const default_backend = 'django';

export const useBackendStore = defineStore("backend", {
    state: () => ({
        selected_backend: useStorage('backend', null)
    }),
    getters: {
        backend(state) {
            return backends[state.selected_backend] || backends[default_backend];
        },

        backendUrl(state) {
            return this.backend.url;
        },

        backends() {
            return backends;
        }
    },

    actions: {
        selectBackend(backend_name) {
            this.selected_backend = backend_name;
        },

    },
});
