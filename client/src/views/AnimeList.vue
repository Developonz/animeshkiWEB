<template>
  <div>
    <h1>Anime List</h1>
    <ul>
      <li v-for="anime in animes" :key="anime.id">
        <router-link :to="{ name: 'AnimeDetail', params: { id: anime.id } }">{{ anime.title }}</router-link>
      </li>
    </ul>
    <router-link to="/anime/create">Create New Anime</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const animes = ref([]);

onMounted(async () => {
  const response = await axios.get('/api/animes/');
  animes.value = response.data;
});
</script> 