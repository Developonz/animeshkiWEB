<template>
    <div class="container mt-5">
      <h1 class="mb-4">Жанры</h1>
  
      <!-- Форма для добавления нового жанра -->
      <form @submit.prevent="onGenreAdd" v-if="is_auth && is_staff"> 
        <div class="row align-items-end">
          <!-- Поле Название жанра -->
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="genreToAdd.name"
                required
                placeholder="Название жанра"
              />
              <label>Название жанра</label>
            </div>
          </div>
          <div class="col d-flex justify-content-end">
            <button type="submit" class="btn btn-primary">
              Добавить
            </button>
          </div>
        </div>
      </form>

      <div class="card mb-4 mt-4">
        <div class="card-body">
          <h5 class="card-title">Статистика жанров</h5>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <strong>Всего жанров: </strong> {{ genreStats['Всего жанров:'] || 0 }}
            </li>
            <li class="list-group-item">
              <strong>Наиболее популярный жанр: </strong> {{ genreStats['Наиболее популярный жанр:'] || '-' }}
            </li>
            <li class="list-group-item">
              <strong>Наименее популярный жанр: </strong> {{ genreStats['Наименее популярный жанр:'] || '-' }}
            </li>
          </ul>
        </div>
      </div>
  
      <!-- Список жанров -->
      <table class="table table-striped mt-5">
        <thead>
          <tr>
            <th>Название жанра</th>
            <th class="col-md-1">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="genre in genres" :key="genre.id">
            <td>{{ genre.name }}</td>
            <td>
              <button
                class="btn btn-success btn-sm me-2"
                @click="onGenreEdit(genre)"
                data-bs-toggle="modal"
                data-bs-target="#editGenreModal"
                title="Редактировать"
              >
                <i class="bi bi-pen-fill"></i>
              </button>
              <button
                class="btn btn-danger btn-sm"
                @click="onGenreDelete(genre.id)"
                title="Удалить"
              >
                <i class="bi bi-x"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Модальное окно для редактирования -->
      <div
        class="modal fade"
        id="editGenreModal"
        tabindex="-1"
        aria-labelledby="editGenreModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="onGenreUpdate">
              <div class="modal-header">
                <h5 class="modal-title" id="editGenreModalLabel">
                  Редактировать жанр
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Закрыть"
                ></button>
              </div>
              <div class="modal-body">
                <div class="form-floating mb-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="genreToEdit.name"
                    required
                    placeholder="Название жанра"
                  />
                  <label>Название жанра</label>
                </div>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeModal"
                >
                  Отмена
                </button>
                <button type="submit" class="btn btn-primary">
                  Сохранить
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import Cookies from 'js-cookie';
  import { Modal } from 'bootstrap';

  import { useUserProfileStore } from "@/stores/UserProfileStore";
  import { storeToRefs } from 'pinia';

  const userProfileStore = useUserProfileStore();
  const { is_auth, username, is_superuser, is_staff } = storeToRefs(userProfileStore);
  
  // Реактивные переменные
  const genres = ref([]);
  const genreToAdd = ref({
    name: '',
  });
  const genreToEdit = ref({
    id: null,
    name: '',
  });
  
  // Экземпляр модального окна
  const editModal = ref(null);

  const genreStats = ref({});

  async function fetchGenreStats() {
    try {
      const response = await axios.get('/api/genres/stats/');
      genreStats.value = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке статистики жанров:', error);
    }
  }
  
  // Функции загрузки данных с бэкенда
  async function fetchGenres() {
    try {
      const response = await axios.get('/api/genres/');
      genres.value = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке жанров:', error);
      alert('Не удалось загрузить жанры.');
    }
  }
  
  // Функция добавления нового жанра
  async function onGenreAdd() {
    // Проверка на существующее название
    const existingGenre = genres.value.find(
      g => g.name.toLowerCase() === genreToAdd.value.name.toLowerCase()
    );
    
    if (existingGenre) {
      alert('Жанр с таким названием уже существует');
      return;
    }

    try {
      await axios.post('/api/genres/', genreToAdd.value);
      await fetchGenres();
      genreToAdd.value = { name: '' };
    } catch (error) {
      handleError(error, 'добавлении жанра');
    }
  }
  
  // Функция подготовки к редактированию жанра
  function onGenreEdit(genre) {
    genreToEdit.value = { ...genre };
    // Показать модальное окно после подготовки данных
    editModal.value.show();
  }
  
  // Функция обновления жанра
  async function onGenreUpdate() {
    // Проверка на существующее название
    const existingGenre = genres.value.find(
      g => g.name.toLowerCase() === genreToEdit.value.name.toLowerCase() 
      && g.id !== genreToEdit.value.id
    );
    
    if (existingGenre) {
      alert('Жанр с таким названием уже существует');
      return;
    }

    try {
      await axios.put(`/api/genres/${genreToEdit.value.id}/`, genreToEdit.value);
      await fetchGenres();
      closeModal();
    } catch (error) {
      handleError(error, 'обновлении жанра');
    }
  }
  
  // Функция удаления жанра
  async function onGenreDelete(id) {
    if (!confirm('Вы уверены, что хотите удалить этот жанр?')) {
      return;
    }
  
    try {
      await axios.delete(`/api/genres/${id}/`);
      await fetchGenres();
    } catch (error) {
      console.error('Ошибка при удалении жанра:', error);
      alert('Не удалось удалить жанр.');
    }
  }
  
  // Функция для обработки ошибок
  function handleError(error, context) {
    if (error.response && error.response.data) {
      const errorMessages = [];
      for (const [field, messages] of Object.entries(error.response.data)) {
        errorMessages.push(`${field}: ${messages.join(', ')}`);
      }
      alert(`Ошибка при ${context}:\n${errorMessages.join('\n')}`);
    } else {
      console.error(error);
      alert(`Произошла неизвестная ошибка при ${context}.`);
    }
  }
  
  // Загрузка данных при монтировании компонента
  onMounted(() => {
    userProfileStore.fetchUserProfile();
    
    fetchGenres();
    // Установка CSRF токена
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchGenreStats();
  
    // Инициализация модального окна
    const modalElement = document.getElementById('editGenreModal');
    editModal.value = new Modal(modalElement, {
      backdrop: 'static', // Не закрывать при клике на backdrop
      keyboard: false, // Не закрывать при нажатии клавиши Esc
    });
  });
  
  // Добавить функцию closeModal
  function closeModal() {
    const modalElement = document.getElementById('editGenreModal');
    const modalInstance = Modal.getInstance(modalElement);
    modalInstance.hide();
    setTimeout(() => {
      const backdrops = document.querySelectorAll('.modal-backdrop');
      backdrops.forEach(backdrop => backdrop.remove());
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    }, 150);
  }
  </script>
    <style scoped>
  /* Дополнительные стили при необходимости */
  </style>
  
