import axios from "axios";
import {useUserStore} from "@/stores/user.js";
import {useMessagingStore} from "@/stores/messaging.js";

const http = axios.create({
    baseURL: "http://192.168.1.55:8000/api",
    headers: {
        Accept: "application/json",
    },
});

http.interceptors.request.use((config) => {
    messagingStore.activateLoader();
    const token = useUserStore().token;
    if (token) {
        config.headers['Authorization'] = 'Token ' + token;
    }
    return config;
});


http.interceptors.response.use(
    (res) => {
        if (res.data.message) {
            messagingStore.setSuccessMessage(res.data.message);
        }
        messagingStore.deactivateLoader();
        return Promise.resolve(res.data);
    },
    (err) => {
        if (err.message || err.data.message) {
            messagingStore.setErrorMessage(err.message || err.data.message);
        }
        messagingStore.deactivateLoader();
        return Promise.reject(err);
    }
);


export default http;
