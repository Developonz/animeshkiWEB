<!-- AnimeDetail.vue -->
<template>
    <div class="container mt-5" v-if="anime">
      <h1 class="mb-4">{{ anime.title_name }}</h1>
      <div class="row">
        <div class="col-md-4">
          <img 
            :src="anime.picture_url || '/media/noIMG.jpg'" 
            class="img-fluid" 
            alt="Изображение аниме" 
          />
        </div>
        <div class="col-md-8">
          <p><strong>Статус:</strong> {{ getStatusName(anime.status) }}</p>
          <p><strong>Дата выпуска:</strong> {{ formatDate(anime.date) }}</p>
          <p><strong>Студия:</strong> {{ getStudioName(anime.studio) }}</p>
          <p><strong>Режиссер:</strong> {{ getDirectorName(anime.director) }}</p>
          <p><strong>Жанры:</strong> {{ getGenreNames(anime.genres).join(', ') || 'Не указаны' }}</p>
        </div>
      </div>
      <button class="btn btn-secondary mt-3" @click="$router.go(-1)">Назад</button>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const anime = ref(null);
  
  // Реактивные переменные для связанных данных
  const statuses = ref([]);
  const studios = ref([]);
  const directors = ref([]);
  const genresList = ref([]);
  
  // Функция загрузки аниме по ID
  async function fetchAnime() {
    const animeId = route.params.id;
    try {
      const response = await axios.get(`/api/animes/${animeId}/`);
      anime.value = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке аниме:', error);
      alert('Не удалось загрузить информацию об аниме.');
    }
  }
  
  // Функция загрузки статусов
  async function fetchStatuses() {
    try {
      const response = await axios.get('/api/statuses/');
      statuses.value = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке статусов:', error);
      alert('Не удалось загрузить статусы.');
    }
  }
  
  // Функция загрузки студий
  async function fetchStudios() {
    try {
      const response = await axios.get('/api/studios/');
      studios.value = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке студий:', error);
      alert('Не удалось загрузить студии.');
    }
  }
  
  // Функция загрузки директоров
  async function fetchDirectors() {
    try {
      const response = await axios.get('/api/directors/');
      directors.value = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке директоров:', error);
      alert('Не удалось загрузить директоров.');
    }
  }
  
  // Функция загрузки жанров
  async function fetchGenresList() {
    try {
      const response = await axios.get('/api/genres/');
      genresList.value = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке жанров:', error);
      alert('Не удалось загрузить жанры.');
    }
  }
  
  // Вызов функций при монтировании компонента
  onMounted(async () => {
    await fetchAnime();
    await fetchStatuses();
    await fetchStudios();
    await fetchDirectors();
    await fetchGenresList();
  });
  
  // Вспомогательные функции для получения имен по ID
  function getStatusName(statusId) {
    const status = statuses.value.find(s => s.id === statusId);
    return status ? status.name : 'Не указан';
  }
  
  function getStudioName(studioId) {
    const studio = studios.value.find(s => s.id === studioId);
    return studio ? studio.name : 'Не выбрано';
  }
  
  function getDirectorName(directorId) {
    const director = directors.value.find(d => d.id === directorId);
    return director ? director.name : 'Не выбран';
  }
  
  function getGenreNames(genreIds) {
    return genresList.value
      .filter(g => genreIds.includes(g.id))
      .map(g => g.name);
  }
  
  // Функция форматирования даты
  function formatDate(dateStr) {
    if (!dateStr) return 'Не указана';
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateStr).toLocaleDateString(undefined, options);
  }
  </script>
  
  <style scoped>
  /* Добавьте стили по необходимости */
  </style>
  