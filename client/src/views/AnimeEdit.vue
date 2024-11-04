<template>
  <div>
    <h1>Edit Anime</h1>
    <form @submit.prevent="updateAnime">
      <input v-model="anime.title" placeholder="Title" required />
      <textarea v-model="anime.description" placeholder="Description" required></textarea>
      <button type="submit">Update</button>
    </form>
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

const updateAnime = async () => {
  await axios.put(`/api/animes/${route.params.id}/`, anime.value);
  router.push({ name: 'AnimeDetail', params: { id: anime.id } });
};
</script>