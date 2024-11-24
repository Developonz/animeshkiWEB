<template>
  <div class="container mt-5">
    <h1 class="mb-4">Аниме</h1>

    <!-- Форма для добавления нового аниме -->
    <form @submit.prevent="onAnimeAdd">
      <!-- Первая строка полей -->
      <div class="row align-items-end">

        <!-- Поле Название -->
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="animeToAdd.title_name"
              required
              placeholder="Название"
            />
            <label>Название</label>
          </div>
        </div>

        <!-- Поле Статус -->
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="animeToAdd.status" required>
              <option disabled value="">Выберите статус</option>
              <option
                v-for="status in statuses"
                :key="status.id"
                :value="status.id"
              >
                {{ status.name }}
              </option>
            </select>
            <label>Статус</label>
          </div>
        </div>

        <!-- Поле Дата выпуска -->
        <div class="col">
          <div class="form-floating">
            <input
              type="date"
              class="form-control"
              v-model="animeToAdd.date"
              placeholder="Дата выпуска"
              :required="!isAnnouncement"
            />
            <label>Дата выпуска</label>
          </div>
        </div>

        <!-- Поле Студия -->
        <div class="col">
          <div class="form-floating">
            <select 
              class="form-select" 
              v-model="animeToAdd.studio"
              :required="!isAnnouncement"
            >
              <option :value="null">Не выбрано</option>
              <option
                v-for="studio in studios"
                :key="studio.id"
                :value="studio.id"
              >
                {{ studio.name }}
              </option>
            </select>
            <label>Студия</label>
          </div>
        </div>

        <!-- Поле Директор -->
        <div class="col">
          <div class="form-floating">
            <select 
              class="form-select" 
              v-model="animeToAdd.director"
              :required="!isAnnouncement"
            >
              <option :value="null">Не выбрано</option>
              <option
                v-for="director in directors"
                :key="director.id"
                :value="director.id"
              >
                {{ director.name }}
              </option>
            </select>
            <label>Директор</label>
          </div>
        </div>
      </div>

      <!-- Вторая строка полей (жанры) -->
      <div class="row align-items-end mt-3">
        <!-- Поле Жанры с двумя списками и одной кнопкой -->
        <div class="col">
          <label class="form-label">Жанры</label>
          <div class="d-flex">
            <div class="fixed-width me-2">
              <select
                class="form-select"
                multiple
                size="5"
                v-model="selectedAvailableGenresAdd"
              >
                <option
                  v-for="genre in availableGenresAdd"
                  :key="genre.id"
                  :value="genre.id"
                >
                  {{ genre.name }}
                </option>
              </select>
            </div>
            <div class="d-flex flex-column justify-content-center">
              <button
                type="button"
                class="btn btn-secondary mb-2"
                @click="toggleGenresAdd"
                :disabled="!selectedAvailableGenresAdd.length && !selectedSelectedGenresAdd.length"
                title="Переместить выбранные жанры"
              >
                ↔
              </button>
            </div>
            <div class="fixed-width ms-2">
              <select
                class="form-select"
                multiple
                size="5"
                v-model="selectedSelectedGenresAdd"
              >
                <option
                  v-for="genre in selectedGenresAdd"
                  :key="genre.id"
                  :value="genre.id"
                >
                  {{ genre.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Третья строка: изображение и кнопка Добавить -->
      <div class="row mt-3">
        <div class="col d-flex justify-content-end">
          <div class="col-auto me-3">
            <img :src="animeAddImageUrl" alt="Изображение" style="max-height: 60px; max-width: 60px;" v-if="animeAddImageUrl"/>
          </div>
          <div class="col-auto me-3">
            <input type="file" class="form-control" ref="animesPictureRef" @change="animesAddPictureChange"/>
          </div>
          <button type="submit" class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <!-- Список аниме -->
    <table class="table table-striped mt-5">
      <thead>
        <tr>
          <th>Название</th>
          <th>Дата выпуска</th>
          <th>Студия</th>
          <th>Директор</th>
          <th>Жанры</th>
          <th>Статус</th>
          <th class="col-2">Изображение</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="anime in animes" :key="anime.id">
          <td>{{ anime.title_name }}</td>
          <td>{{ formatDate(anime.date) }}</td>
          <td>{{ getStudioName(anime.studio) }}</td>
          <td>{{ getDirectorName(anime.director) }}</td>
          <td>{{ getGenreNames(anime.genres).join(', ') }}</td>
          <td>{{ getStatusName(anime.status) }}</td>
          <td>
            <div v-if="anime.picture">
              <img 
                :src="getFullImageUrl(anime.picture)" 
                style="max-height: 60px; max-width: 60px; cursor: pointer;" 
                alt="Изображение аниме"
                @click="showImage(getFullImageUrl(anime.picture))"
              />
            </div>
          </td>
          <td>
            <button
              class="btn btn-success btn-sm me-2"
              @click="onAnimeEdit(anime)"
              data-bs-toggle="modal"
              data-bs-target="#editAnimeModal"
              title="Редактировать"
            >
              <i class="bi bi-pen-fill"></i>
            </button>
            <button
              class="btn btn-danger btn-sm"
              @click="onAnimeDelete(anime.id)"
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
      id="editAnimeModal"
      tabindex="-1"
      aria-labelledby="editAnimeModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="onAnimeUpdate">
            <div class="modal-header">
              <h5 class="modal-title" id="editAnimeModalLabel">
                Редактироть аниме
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">

              <!-- Первая строка полей: Название -->
              <div class="form-floating mb-3">
                <input
                  type="text"
                  class="form-control"
                  v-model="animeToEdit.title_name"
                  required
                  placeholder="Название"
                />
                <label>Название</label>
              </div>

              <!-- Вторая строка полей: Статус, Дата выпуска-->
              <div class="row">
                <!-- Поле Статус -->
                <div class="col">
                  <div class="form-floating mb-3">
                    <select
                      class="form-select"
                      v-model="animeToEdit.status"
                      required
                    >
                      <option disabled value="">Выберите статус</option>
                      <option
                        v-for="status in statuses"
                        :key="status.id"
                        :value="status.id"
                      >
                        {{ status.name }}
                      </option>
                    </select>
                    <label>Статус</label>
                  </div>
                </div>

                <!-- Поле Дата выпуска -->
                <div class="col">
                  <div class="form-floating mb-3">
                    <input
                      type="date"
                      class="form-control"
                      v-model="animeToEdit.date"
                      placeholder="Дата выпуска"
                      :required="!isAnnouncementEdit"
                    />
                    <label>Дата выпуска</label>
                  </div>
                </div>
              </div>
              <!-- Третья строка полей: Директор, Студия  -->
              <div class="row">
                <div class="col">
                  <div class="form-floating mb-3">
                    <select 
                      class="form-select" 
                      v-model="animeToEdit.director"
                      :required="!isAnnouncementEdit"
                    >
                      <option :value="null">Не выбрано</option>
                      <option
                        v-for="director in directors"
                        :key="director.id"
                        :value="director.id"
                      >
                        {{ director.name }}
                      </option>
                    </select>
                    <label>Директор</label>
                  </div>
                </div>
                <!-- Поле Студия -->
                <div class="col">
                  <div class="form-floating mb-3">
                    <select 
                      class="form-select" 
                      v-model="animeToEdit.studio"
                      :required="!isAnnouncementEdit"
                    >
                      <option :value="null">Не выбрано</option>
                      <option
                        v-for="studio in studios"
                        :key="studio.id"
                        :value="studio.id"
                      >
                        {{ studio.name }}
                      </option>
                    </select>
                    <label>Студия</label>
                  </div>
                </div>
              </div>

              <!-- Четвёртая строка: Поле Жанры с двумя списками и одной кнопкой -->
              <div class="form-group mb-3">
                <label class="form-label">Жанры</label>
                <div class="d-flex">
                  <div class="fixed-width me-2">
                    <select
                      class="form-select"
                      multiple
                      size="5"
                      v-model="selectedAvailableGenresEdit"
                    >
                      <option
                        v-for="genre in availableGenresEdit"
                        :key="genre.id"
                        :value="genre.id"
                      >
                        {{ genre.name }}
                      </option>
                    </select>
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <button
                      type="button"
                      class="btn btn-secondary"
                      @click="toggleGenresEdit"
                      :disabled="!selectedAvailableGenresEdit.length && !selectedSelectedGenresEdit.length"
                      title="Переместить выбранные жанры"
                    >
                      ↔
                    </button>
                  </div>
                  <div class="fixed-width ms-2">
                    <select
                      class="form-select"
                      multiple
                      size="5"
                      v-model="selectedSelectedGenresEdit"
                    >
                      <option
                        v-for="genre in selectedGenresEdit"
                        :key="genre.id"
                        :value="genre.id"
                      >
                        {{ genre.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Пятая строка Изображение -->
              <div class="row mt-3">
                <div class="col">
                  <div class="d-flex align-items-center justify-content-end">
                    <img 
                      :src="animeAddImageEditUrl || animeToEdit.picture" 
                      alt="Изображение" 
                      style="max-height: 60px; max-width: 60px;" 
                      v-if="animeAddImageEditUrl || animeToEdit.picture"
                      class="me-2"
                    />
                    <button 
                      type="button" 
                      class="btn btn-danger btn-sm me-2" 
                      @click="removePicture" 
                      v-if="animeAddImageEditUrl || animeToEdit.picture"
                      title="Удалить изображение"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                    <input type="file" class="form-control w-auto" ref="animesPictureToEditRef" @change="animesAddPictureEditChange"/>
                  </div>
                </div>
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

    <!-- Добавить в template после основного модального окна -->
    <div class="modal fade" id="imageModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body p-0">
            <button type="button" class="btn-close position-absolute top-0 end-0 m-2" data-bs-dismiss="modal"></button>
            <img :src="selectedImage" class="img-fluid" alt="Увеличенное изображение">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Modal } from 'bootstrap';

/* 
import {storeToRefs} from "pinia";
import useUserProfileStore from "@/stores/UserProfileStore";
const userProfileStore = useUserProfileStore();
const {is_auth, username, is_superuser} = storeToRefs(userProfileStore); 
*/



// Реативные переменные
const animes = ref([]);
const animeToAdd = ref({
  title_name: '',
  date: '',
  studio: null,
  director: null,
  genres: [],
  status: '',
});
const animeToEdit = ref({
  id: null,
  title_name: '',
  date: '',
  studio: null,
  director: null,
  genres: [],
  status: '',
});
const genres = ref([]);
const studios = ref([]);
const directors = ref([]);
const statuses = ref([]);

// Для поя жанров в добавлении
const availableGenresAdd = ref([]);
const selectedGenresAdd = ref([]);
const selectedAvailableGenresAdd = ref([]);
const selectedSelectedGenresAdd = ref([]);

// Для поля жанров в редактировании
const availableGenresEdit = ref([]);
const selectedGenresEdit = ref([]);
const selectedAvailableGenresEdit = ref([]);
const selectedSelectedGenresEdit = ref([]);

// Новые реактивные переменные
const animesPictureRef = ref();
const animeAddImageUrl = ref();
const animesPictureToEditRef = ref();
const animeAddImageEditUrl = ref();

// Экземпляр модального окна
const editModal = ref(null);

// Добавьте вычисляемое свойство
const isAnnouncement = computed(() => {
  const announcementStatus = statuses.value.find(s => s.name.toLowerCase() === 'анонс');
  return animeToAdd.value.status === announcementStatus?.id;
});

const isAnnouncementEdit = computed(() => {
  const announcementStatus = statuses.value.find(s => s.name.toLowerCase() === 'анонс');
  return animeToEdit.value.status === announcementStatus?.id;
});

// Функции загрузки данных с бэкенда
async function fetchAnimes() {
  try {
    const response = await axios.get('/api/animes/');
    animes.value = response.data;
    console.log('Полученные аниме:', animes.value);
  } catch (error) {
    console.error('Ошибка при загрузке аниме:', error);
    alert('Не удалось загрузить список аниме.');
  }
}

async function fetchGenres() {
  try {
    const response = await axios.get('/api/genres/');
    genres.value = response.data;
    availableGenresAdd.value = [...genres.value];
  } catch (error) {
    console.error('Ошибка при загрузке жанров:', error);
    alert('Не удалось загрузить жанры.');
  }
}

async function fetchStudios() {
  try {
    const response = await axios.get('/api/studios/');
    studios.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке студий:', error);
    alert('Не удалось агрузить студии.');
  }
}

async function fetchDirectors() {
  try {
    const response = await axios.get('/api/directors/');
    directors.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке директоров:', error);
    alert('Не удалось загрузить директоров.');
  }
}

async function fetchStatuses() {
  try {
    const response = await axios.get('/api/statuses/');
    statuses.value = response.data;
    console.log('Статусы:', statuses.value);
  } catch (error) {
    console.error('Ошибка при загрузке статусов:', error);
    alert('Не удалось загрузить статусы.');
  }
}

// Новые методы для обработки изображений
async function animesAddPictureChange() {
  animeAddImageUrl.value = URL.createObjectURL(animesPictureRef.value.files[0]);
}

async function animesAddPictureEditChange() {
  animeAddImageEditUrl.value = URL.createObjectURL(animesPictureToEditRef.value.files[0]);
}

// Функция добавления нового аниме
async function onAnimeAdd() {
  if (selectedGenresAdd.value.length === 0) {
    alert('Пожалуйста, выберите хотя бы один жанр.');
    return;
  }

  const formData = new FormData();
  
  formData.append('title_name', animeToAdd.value.title_name);
  formData.append('status', animeToAdd.value.status);
  
  if (animeToAdd.value.date) {
    formData.append('date', new Date(animeToAdd.value.date).toISOString().split('T')[0]);
  }
  
  if (animeToAdd.value.studio) {
    formData.append('studio', animeToAdd.value.studio);
  }
  if (animeToAdd.value.director) {
    formData.append('director', animeToAdd.value.director);
  }

  selectedGenresAdd.value.forEach(genre => {
    formData.append('genres', genre.id);
  });

  if (animesPictureRef.value.files[0]) {
    formData.append('picture', animesPictureRef.value.files[0]);
  }

  try {
    await axios.post('/api/animes/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    animeAddImageUrl.value = null;
    await fetchAnimes();
    resetAddForm();
  } catch (error) {
    handleError(error, 'добавлении аниме');
  }
}

// Функция сброса формы добавления
function resetAddForm() {
  animeToAdd.value = {
    title_name: '',
    date: '',
    studio: null,
    director: null,
    genres: [],
    status: '',
  };
  // Сброс жанров
  availableGenresAdd.value = [...genres.value];
  selectedGenresAdd.value = [];
  selectedAvailableGenresAdd.value = [];
  selectedSelectedGenresAdd.value = [];
}

// Функция подготовки к редактированию аниме
function onAnimeEdit(anime) {
  animeToEdit.value = { ...anime };
  // Сбрасываем URL временного изображения при открытии формы редактирования
  animeAddImageEditUrl.value = null;
  selectedGenresEdit.value = genres.value.filter((genre) =>
    anime.genres.includes(genre.id)
  );
  availableGenresEdit.value = genres.value.filter(
    (genre) => !anime.genres.includes(genre.id)
  );
  selectedAvailableGenresEdit.value = [];
  selectedSelectedGenresEdit.value = [];
  // Показать модальное окно после подготовки данных
  editModal.value.show();
}

// Функция обновления аниме
async function onAnimeUpdate() {
  if (selectedGenresEdit.value.length === 0) {
    alert('Пожалуйста, выберите хотя бы один жанр.');
    return;
  }

  const formData = new FormData();
  formData.append('title_name', animeToEdit.value.title_name);
  formData.append('status', animeToEdit.value.status);
  
  if (animeToEdit.value.date) {
    formData.append('date', new Date(animeToEdit.value.date).toISOString().split('T')[0]);
  }
  
  if (animeToEdit.value.studio) {
    formData.append('studio', animeToEdit.value.studio);
  }
  if (animeToEdit.value.director) {
    formData.append('director', animeToEdit.value.director);
  }

  selectedGenresEdit.value.forEach(genre => {
    formData.append('genres', genre.id);
  });

  if (animesPictureToEditRef.value?.files[0]) {
    formData.append('picture', animesPictureToEditRef.value.files[0]);
  } else if (animeToEdit.value.picture === null) {
    formData.append('picture', '');
  }

  try {
    await axios.put(`/api/animes/${animeToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchAnimes();
    // Очищаем поле с картинкой после успешного обновления
    animeAddImageEditUrl.value = null;
    if (animesPictureToEditRef.value) {
      animesPictureToEditRef.value.value = '';
    }
    closeModal();
  } catch (error) {
    handleError(error, 'обновлении аниме');
  }
}

// Функция удаления аниме
async function onAnimeDelete(id) {
  if (!confirm('Вы уверены, что хотите удалить это аниме?')) {
    return;
  }

  try {
    await axios.delete(`/api/animes/${id}/`);
    await fetchAnimes();
  } catch (error) {
    console.error('Ошибка при удалении аниме:', error);
    alert('Не удалось удалить аниме.');
  }
}

// Функция переключения жанров в добавлении
function toggleGenresAdd() {
  if (selectedAvailableGenresAdd.value.length > 0) {
    // Перемещение из доступных в выбранные
    selectedAvailableGenresAdd.value.forEach((genreId) => {
      const genre = availableGenresAdd.value.find((g) => g.id === genreId);
      if (genre) {
        selectedGenresAdd.value.push(genre);
        availableGenresAdd.value = availableGenresAdd.value.filter(
          (g) => g.id !== genreId
        );
      }
    });
    selectedAvailableGenresAdd.value = [];
  } else if (selectedSelectedGenresAdd.value.length > 0) {
    // Перемещение из выбранных в доступные
    selectedSelectedGenresAdd.value.forEach((genreId) => {
      const genre = selectedGenresAdd.value.find((g) => g.id === genreId);
      if (genre) {
        availableGenresAdd.value.push(genre);
        selectedGenresAdd.value = selectedGenresAdd.value.filter(
          (g) => g.id !== genreId
        );
      }
    });
    selectedSelectedGenresAdd.value = [];
  }
}

// Функция переключения жанров в редактировании
function toggleGenresEdit() {
  if (selectedAvailableGenresEdit.value.length > 0) {
    // Перемещение из доступных в выбранные
    selectedAvailableGenresEdit.value.forEach((genreId) => {
      const genre = availableGenresEdit.value.find((g) => g.id === genreId);
      if (genre) {
        selectedGenresEdit.value.push(genre);
        availableGenresEdit.value = availableGenresEdit.value.filter(
          (g) => g.id !== genreId
        );
      }
    });
    selectedAvailableGenresEdit.value = [];
  } else if (selectedSelectedGenresEdit.value.length > 0) {
    // Перемщение из выбранных в доступные
    selectedSelectedGenresEdit.value.forEach((genreId) => {
      const genre = selectedGenresEdit.value.find((g) => g.id === genreId);
      if (genre) {
        availableGenresEdit.value.push(genre);
        selectedGenresEdit.value = selectedGenresEdit.value.filter(
          (g) => g.id !== genreId
        );
      }
    });
    selectedSelectedGenresEdit.value = [];
  }
}

// Вспомогательные функции для отображения имен
function getGenreNames(genreIds) {
  return genres.value
    .filter((genre) => genreIds.includes(genre.id))
    .map((genre) => genre.name);
}

function getStudioName(studioId) {
  const studio = studios.value.find((studio) => studio.id === studioId);
  return studio ? studio.name : 'Не выбрано';
}

function getDirectorName(directorId) {
  const director = directors.value.find(
    (director) => director.id === directorId
  );
  return director ? director.name : 'Не выбрано';
}

function getStatusName(statusId) {
  const status = statuses.value.find((status) => status.id === statusId);
  return status ? status.name : 'Не выбрано';
}

function formatDate(dateStr) {
  if (!dateStr) return 'Не указана';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateStr).toLocaleDateString(undefined, options);
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

// Добавьте новую функцию для получения полного URL изображения
function getImageUrl(relativePath) {
  if (!relativePath) return null;
  
  // Если путь уже начинается с http или https
  if (relativePath.startsWith('http://') || relativePath.startsWith('https://')) {
    return relativePath;
  }
  
  // Для относительных путей добавляем базовый URL Django сервера
  const baseUrl = 'http://localhost:8000';
  // Убираем дублирующиеся слеши
  const cleanPath = relativePath.startsWith('/') ? relativePath : '/' + relativePath;
  
  return `${baseUrl}${cleanPath}`;
}

// Загрузка данных при монтировании компонента
onMounted(() => {
  fetchAnimes();
  fetchGenres();
  fetchStudios();
  fetchDirectors();
  fetchStatuses();
  // Установка CSRF токена
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

  // Инициализация модального окна
  const modalElement = document.getElementById('editAnimeModal');
  editModal.value = new Modal(modalElement, {
    backdrop: 'static', // Не закрывать при клике на backdrop
    keyboard: false, // Не закрывать при нажатии клавиши Esc
  });

  // Инициализация модального окна для изображения
  const imageModalElement = document.getElementById('imageModal');
  imageModal.value = new Modal(imageModalElement, {
    backdrop: 'static', // Не закрывать при клике на backdrop
    keyboard: false, // Не закрывать при нажатии клавиши Esc
  });
});

// В script setup добавим функцию
function getFullImageUrl(url) {
  if (!url) return '';
  // Если URL абсолютный
  if (url.startsWith('http')) return url;
  
  // Добавим console.log для отладки
  const fullUrl = `${import.meta.env.VITE_API_URL}${url}`;
  console.log('Image URL:', fullUrl);
  return fullUrl;
}

// Добавить функцию closeModal
function closeModal() {
  const modalElement = document.getElementById('editAnimeModal');
  const modalInstance = Modal.getInstance(modalElement);
  modalInstance.hide();
  
  // Очистка полей изображения
  animeAddImageEditUrl.value = null;
  if (animesPictureToEditRef.value) {
    animesPictureToEditRef.value.value = '';
  }
  
  setTimeout(() => {
    const backdrops = document.querySelectorAll('.modal-backdrop');
    backdrops.forEach(backdrop => backdrop.remove());
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
  }, 150);
}

// В script setup добавить функцию
function removePicture() {
  animeToEdit.value.picture = null;
  animeAddImageEditUrl.value = null;
  if (animesPictureToEditRef.value) {
    animesPictureToEditRef.value.value = '';
  }
}

// В script setup добавить
const selectedImage = ref('');
const imageModal = ref(null);

function showImage(imageUrl) {
  selectedImage.value = imageUrl;
  const modal = new Modal(document.getElementById('imageModal'));
  modal.show();
}
</script>

<style lang="scss" scoped>

/* Фиксированные размеры для полей выбора жанров */
.fixed-width {
  width: 50%; 
}

.fixed-width select {
  width: 100%;
}
/* Дополнительные стили при необходимости */
.form-label {
  margin-bottom: 0.5rem;
}
</style>
