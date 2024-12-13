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

    <!-- Блок для отображения статистики -->
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
          <th class="col-md-1" v-if="is_superuser">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="genre in genres" :key="genre.id">
          <td>{{ genre.name }}</td>
          <td v-if="is_superuser">
            <button
              class="btn btn-success btn-sm me-2"
              @click="onGenreEdit(genre)"
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
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="onGenreUpdate">
            <div class="modal-header">
              <h5 class="modal-title" id="editGenreModalLabel">
                Редактировать жанр
              </h5>
              <button
                type="button"
                class="btn-close"
                @click="closeModal"
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

    <!-- Модальное окно для просмотра изображения -->
    <div class="modal fade" id="imageModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body p-0">
            <button 
              type="button" 
              class="btn-close position-absolute top-0 end-0 m-2" 
              @click="closeImageModal" 
              aria-label="Закрыть"
            ></button>
            <img 
              :src="selectedImage" 
              class="img-fluid" 
              alt="Увеличенное изображение"
              @contextmenu.prevent
              draggable="false"
            />
          </div>
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

// Реактивные переменные для изображений (если необходимо)
const genrePictureToEditRef = ref();
const genreAddImageEditUrl = ref();

// Экземпляры модальных окон
const editModal = ref(null);
const imageModal = ref(null);

// Статистика жанров
const genreStats = ref({});

// Вспомогательные переменные для просмотра изображения
const selectedImage = ref('');

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

async function fetchGenreStats() {
  try {
    const response = await axios.get('/api/genres/stats/');
    genreStats.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статистики жанров:', error);
    alert('Не удалось загрузить статистику жанров.');
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
    await fetchGenreStats();
    resetAddForm();
  } catch (error) {
    handleError(error, 'добавлении жанра');
  }
}

// Функция подготовки к редактированию жанра
function onGenreEdit(genre) {
  genreToEdit.value = { ...genre };
  // Сбрасываем URL временного изображения при открытии формы редактирования (если есть)
  genreAddImageEditUrl.value = null;
  
  // Показать модальное окно через Bootstrap Modal API
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

  const payload = {
    name: genreToEdit.value.name,
  };

  // В данном примере предполагается отправка JSON
  try {
    await axios.put(`/api/genres/${genreToEdit.value.id}/`, payload);
    await fetchGenres();
    await fetchGenreStats();
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
    await fetchGenreStats();
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

// Функции для обработки изображений (если необходимо)
function genreAddPictureEditChange() {
  if (genrePictureToEditRef.value.files[0]) {
    genreAddImageEditUrl.value = URL.createObjectURL(genrePictureToEditRef.value.files[0]);
  } else {
    genreAddImageEditUrl.value = null;
  }
}

// Функция сброса формы добавления
function resetAddForm() {
  genreToAdd.value = {
    name: '',
  };
}

// Функция закрытия модального окна редактирования
function closeModal() {
  editModal.value.hide();
  
  // Очистка полей изображения (если есть)
  genreAddImageEditUrl.value = null;
  if (genrePictureToEditRef.value) {
    genrePictureToEditRef.value.value = '';
  }
}

// Функция для просмотра увеличенного изображения
function showImage(imageUrl) {
  selectedImage.value = imageUrl;
  imageModal.value.show();
}

// Инициализация модальных окон и загрузка данных при монтировании компонента
onMounted(() => {
  userProfileStore.fetchUserProfile();

  fetchGenres();
  fetchGenreStats();
  // Установка CSRF токена
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

  // Инициализация модального окна для редактирования
  const editModalElement = document.getElementById('editGenreModal');
  editModal.value = new Modal(editModalElement, {
    backdrop: 'static', // Не закрывать при клике на backdrop
    keyboard: false, // Не закрывать при нажатии клавиши Esc
  });

  // Инициализация модального окна для просмотра изображения
  const imageModalElement = document.getElementById('imageModal');
  imageModal.value = new Modal(imageModalElement, {
    backdrop: true,
    keyboard: true,
  });
});
</script>

<style scoped>
/* Дополнительные стили при необходимости */
.nav-link.active {
  color: #ff0000 !important;
  background-color: #e0e0e0;
  border-radius: 10px; 
}

.nav-link {
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
}

.nav-link:not(.active):hover {
  border-bottom: 2px solid #0d6efd;
}
</style>
