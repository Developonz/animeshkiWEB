<template>
  <div class="container mt-5">
    <h1 class="mb-4">Аниме</h1>

    <!-- Форма для добавления нового аниме (только для аутентифицированных пользователей) -->
    <form @submit.prevent="onAnimeAdd" v-if="is_auth && is_staff">
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
              placeholder="Студия"
            >
              <option disabled value="">Выберите студию</option>
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
              placeholder="Директор"
            >
              <option disabled value="">Выберите директора</option>
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

    <!-- Фильтр по пользователям и собственному аниме -->
    <div v-if="is_superuser || is_staff" class="mb-4">
      <div class="form-floating">
        <select class="form-select w-25" v-model="userToFilter">
          <!-- Для суперпользователей -->
          <template v-if="is_superuser">
            <option value="all">Все пользователи</option>
            <option 
              v-for="usernameOption in usersToFilter" 
              :key="usernameOption"
              :value="usernameOption"
            >
              {{ usernameOption }}
            </option>
          </template>
          <!-- Для сотрудников -->
          <template v-else-if="is_staff">
            <option value="all">Все аниме</option>
            <option value="my">Мои аниме</option>
          </template>
        </select>
        <label>Фильтр по пользователю</label>
      </div>
    </div>

    <!-- Блок для отображения статистики -->
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Статистика аниме</h5>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <strong>Всего аниме:</strong> {{ animeStats['Всего аниме:'] || 0 }}
          </li>
          <li class="list-group-item">
            <strong>Распределение по статусу:</strong>
            <ul>
              <li v-for="(count, status) in animeStats['Распределение по статусу:']" :key="status">
                {{ status }}: {{ count }}
              </li>
            </ul>
          </li>
          <li class="list-group-item">
            <strong>Максимум аниме в году:</strong>
            <ul>
              <li v-for="(count, year) in animeStats['Максимум аниме в году:']" :key="year">
                {{ year }}: {{ count }}
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>

    <!-- Сетка плиток аниме -->
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
      <div class="col" v-for="anime in animes" :key="anime.id">
        <div class="card h-100 position-relative">
          <!-- Изображение и название как ссылка -->
          <router-link :to="`/anime/${anime.id}`" class="text-decoration-none text-dark">
            <img 
              :src="anime.picture_url || '/media/noIMG.jpg'" 
              class="card-img-top" 
              alt="Изображение аниме" 
              style="height: 200px; object-fit: cover;"
            />
            <div class="card-body text-center"> <!-- Центрируем текст -->
              <h5 class="card-title">{{ anime.title_name }}</h5>
            </div>
          </router-link>

          <!-- Кнопки редактирования и удаления для суперпользователей и сотрудников (только свои аниме для сотрудников) -->
          <div v-if="canEditDelete(anime)" class="position-absolute top-0 end-0 p-2">
            <button 
              class="btn btn-sm btn-success me-1" 
              @click.stop="onAnimeEdit(anime)"
              title="Редактировать"
            >
              <i class="bi bi-pen-fill"></i>
            </button>
            <button 
              class="btn btn-sm btn-danger" 
              @click.stop="onAnimeDelete(anime.id)"
              title="Удалить"
            >
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для редактирования -->
    <div
      class="modal fade"
      id="editAnimeModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="editAnimeModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="onAnimeUpdate">
            <div class="modal-header">
              <h5 class="modal-title" id="editAnimeModalLabel">
                Редактировать аниме
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
                      placeholder="Директор"
                    >
                      <option value="">Выберите директора</option>
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
                      placeholder="Студия"
                    >
                      <option value="">Выберите студию</option>
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
                      :src="animeAddImageEditUrl || animeToEdit.picture_url || '/media/noIMG.jpg'" 
                      alt="Изображение" 
                      style="max-height: 60px; max-width: 60px;" 
                      v-if="animeAddImageEditUrl || animeToEdit.picture_url"
                      class="me-2"
                    />
                    <button 
                      type="button" 
                      class="btn btn-danger btn-sm me-2" 
                      @click="removePicture" 
                      v-if="animeAddImageEditUrl || animeToEdit.picture_url"
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

    <!-- Модальное окно для просмотра изображения -->
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
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Modal } from 'bootstrap';

import { useUserProfileStore } from "@/stores/UserProfileStore";
import { storeToRefs } from 'pinia';

const userProfileStore = useUserProfileStore();
const { is_auth, username, is_superuser, is_staff } = storeToRefs(userProfileStore);

// Реактивные переменные
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

// Для выбора жанров при добавлении
const availableGenresAdd = ref([]);
const selectedGenresAdd = ref([]);
const selectedAvailableGenresAdd = ref([]);
const selectedSelectedGenresAdd = ref([]);

// Для выбора жанров при редактировании
const availableGenresEdit = ref([]);
const selectedGenresEdit = ref([]);
const selectedAvailableGenresEdit = ref([]);
const selectedSelectedGenresEdit = ref([]);

// Новые реактивные переменные для изображений
const animesPictureRef = ref();
const animeAddImageUrl = ref();
const animesPictureToEditRef = ref();
const animeAddImageEditUrl = ref();

// Экземпляры модальных окон
const editModal = ref(null);
const imageModal = ref(null);

// Статистика аниме
const animeStats = ref({});

// Вычисляемые свойства для определения, является ли статус анонсом
const isAnnouncement = computed(() => {
  const announcementStatus = statuses.value.find(s => s.name.toLowerCase() === 'анонс');
  return animeToAdd.value.status === announcementStatus?.id;
});

const isAnnouncementEdit = computed(() => {
  const announcementStatus = statuses.value.find(s => s.name.toLowerCase() === 'анонс');
  return animeToEdit.value.status === announcementStatus?.id;
});

// Реактивные переменные для фильтрации
const userToFilter = ref('all');
const usersToFilter = ref([]);

// Функция загрузки статистики аниме с учетом фильтра
async function fetchAnimeStats() {
  try {
    let url = '/api/animes/stats/';
    if (userToFilter.value) {
      url += `?user=${userToFilter.value}`;
    }
    const response = await axios.get(url);
    animeStats.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статистики аниме:', error);
    alert('Не удалось загрузить статистику аниме.');
  }
}

// Функция загрузки пользователей (только для суперпользователей)
async function fetchUsers() {
  try {
    const response = await axios.get('/api/animes/users/');
    usersToFilter.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке пользователей:', error);
    alert('Не удалось загрузить список пользователей.');
  }
}

// Функция загрузки списка аниме с учетом фильтра
async function fetchAnimes() {
  try {
    let url = '/api/animes/';
    if (userToFilter.value) {
      // Для суперпользователей и сотрудников
      if (is_superuser.value) {
        // Если выбран пользователь (не 'all')
        if (userToFilter.value !== 'all') {
          url += `?user=${userToFilter.value}`;
        }
      } else if (is_staff.value) {
        // Для сотрудников: 'all' или 'my'
        url += `?user=${userToFilter.value}`;
      }
    }
    const response = await axios.get(url);
    animes.value = response.data;

    // Обновляем статистику после получения аниме
    await fetchAnimeStats();
  } catch (error) {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      alert('Пожалуйста, авторизуйтесь для просмотра списка аниме');
    } else {
      console.error('Ошибка при загрузке аниме:', error);
      alert('Не удалось загрузить список аниме.');
    }
  }
}

// Функции загрузки других данных
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
    alert('Не удалось загрузить студии.');
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
  } catch (error) {
    console.error('Ошибка при загрузке статусов:', error);
    alert('Не удалось загрузить статусы.');
  }
}

// Новые методы для обработки изображений
async function animesAddPictureChange() {
  if (animesPictureRef.value.files[0]) {
    animeAddImageUrl.value = URL.createObjectURL(animesPictureRef.value.files[0]);
  } else {
    animeAddImageUrl.value = null;
  }
}

async function animesAddPictureEditChange() {
  if (animesPictureToEditRef.value.files[0]) {
    animeAddImageEditUrl.value = URL.createObjectURL(animesPictureToEditRef.value.files[0]);
  } else {
    animeAddImageEditUrl.value = null;
  }
}

// Функция добавления нового аниме
async function onAnimeAdd() {
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

  selectedGenresAdd.value.forEach(genreId => {
    formData.append('genres', genreId);
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
  // Сброс изображения
  animeAddImageUrl.value = null;
  if (animesPictureRef.value) {
    animesPictureRef.value.value = '';
  }
}

// Функция подготовки к редактированию аниме
function onAnimeEdit(anime) {
  animeToEdit.value = { ...anime };
  // Сброс URL временного изображения при открытии формы редактирования
  animeAddImageEditUrl.value = null;
  
  // Сохранение полных объектов жанров, а не только их ID
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
    // Очистка поля с картинкой после успешного обновления
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
    // Перемещение из выбранных в доступные
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

// Функция закрытия модального окна редактирования
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

// Функция удаления изображения при редактировании
function removePicture() {
  animeToEdit.value.picture = null;
  animeAddImageEditUrl.value = null;
  if (animesPictureToEditRef.value) {
    animesPictureToEditRef.value.value = '';
  }
}

// Модальное окно для просмотра увеличенного изображения
const selectedImage = ref('');
function showImage(imageUrl) {
  selectedImage.value = imageUrl;
  const modal = new Modal(document.getElementById('imageModal'));
  modal.show();
}

// Функция проверки, может ли текущий пользователь редактировать или удалять аниме
function canEditDelete(anime) {
  return is_superuser.value || (is_staff.value && anime.username === username.value);
}

// Отслеживание изменений фильтра по пользователям и собственному аниме
watch(userToFilter, () => {
  fetchAnimes();
});

// Загрузка данных при монтировании компонента
onMounted(async () => {
  await userProfileStore.fetchUserProfile();
  
  if (is_superuser.value) {
    await fetchUsers();
  }
  
  await fetchAnimes();
  fetchGenres();
  fetchStudios();
  fetchDirectors();
  fetchStatuses();
  fetchAnimeStats();
  
  // Установка CSRF токена
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

  // Инициализация модальных окон
  const modalElement = document.getElementById('editAnimeModal');
  editModal.value = new Modal(modalElement, {
    backdrop: 'static',
    keyboard: false,
  });

  const imageModalElement = document.getElementById('imageModal');
  imageModal.value = new Modal(imageModalElement, {
    backdrop: 'static',
    keyboard: false,
  });
});
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

/* Эффект наведения на карточку */
.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: 0.3s;
}

/* Полупрозрачный фон для кнопок */
.card .btn {
  background-color: rgba(255, 255, 255, 0.8);
}

.card .btn:hover {
  background-color: rgba(255, 255, 255, 1);
}

/* Дополнительные стили для кнопок */
.card .btn-success {
  background-color: #28a745 !important;
  border-color: #28a745 !important;
}

.card .btn-danger {
  background-color: #dc3545 !important;
  border-color: #dc3545 !important;
}

/* Стили для изображений внутри карточек */
.card-img-top {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>
