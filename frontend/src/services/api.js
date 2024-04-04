import axios from "axios";
import {useUserStore} from "@/stores/user.js";
import {useMessagingStore} from "@/stores/messaging.js";

const apiurl = import.meta.env.VITE_API_URL;
console.log("API URL", apiurl)
const http = axios.create({
    baseURL: apiurl,
    headers: {
        Accept: "application/json",
    },
});

http.interceptors.request.use((config) => {
    useMessagingStore().activateLoader();
    const token = useUserStore().token;
    if (token) {
        config.headers['Authorization'] = 'Token ' + token;
    }
    return config;
});


http.interceptors.response.use(
    (response) => {
        console.log("API RESPONSE", response);
        const messagingStore = useMessagingStore();
        if (response.data.message) {
            messagingStore.setSuccessMessage(response.data.message);
        }
        messagingStore.deactivateLoader();
        return Promise.resolve(response.data);
    },
    (error) => {
        console.log("API ERROR", error, error.response.data);
        const messagingStore = useMessagingStore();
        let message;
        if (error.response) {
            message = error.response.message || error.response.data
        }
        if (message || error.message) {
            messagingStore.setErrorMessage(message || error.message);
        }
        messagingStore.deactivateLoader();

        return Promise.reject(error);
    }
);


export default http;
