import {defineStore} from "pinia";

const useUserProfileStore = defineStore("userProfile", () => {
    const is_auth = ref();
    const username = ref();
    const is_superuser = ref();

    onBeforeMount(() => {
        const response = axios.get("/api/user/profile/info");
        is_auth.value = response.data.is_authenticated;
        username.value = response.data.username;
    });

    return {is_auth, username, is_superuser};
});

export default useUserProfileStore;
