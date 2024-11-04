<template>
  <div>
    <h1>Create New Anime</h1>
    <form @submit.prevent="createAnime">
      <input v-model="anime.title" placeholder="Title" required />
      <textarea v-model="anime.description" placeholder="Description" required></textarea>
      <button type="submit">Create</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const anime = ref({ title: '', description: '' });

const createAnime = async () => {
  await axios.post('/api/animes/', anime.value);
  router.push({ name: 'AnimeList' });
};
</script> 