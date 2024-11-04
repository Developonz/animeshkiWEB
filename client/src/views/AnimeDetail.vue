<template>
  <div>
    <h1>{{ anime.title }}</h1>
    <p>{{ anime.description }}</p>
    <router-link :to="{ name: 'AnimeEdit', params: { id: anime.id } }">Edit</router-link>
    <button @click="deleteAnime">Delete</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const anime = ref({});

onMounted(async () => {
  const response = await axios.get(`/api/animes/${route.params.id}/`);
  anime.value = response.data;
});

const deleteAnime = async () => {
  await axios.delete(`/api/animes/${route.params.id}/`);
  router.push({ name: 'AnimeList' });
};
</script> 