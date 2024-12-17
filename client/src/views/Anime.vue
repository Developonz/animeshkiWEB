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
                  v-for="genreId in selectedGenresAdd"
                  :key="genreId"
                  :value="genreId"
                >
                  {{ getGenreNameById(genreId) }}
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
            <img 
              :src="animeAddImageUrl" 
              alt="Изображение" 
              style="max-height: 60px; max-width: 60px;" 
              v-if="animeAddImageUrl"
              @contextmenu.prevent
              draggable="false"
            />
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

    <!-- Фильтры режиссёры, студии, статусы -->
    <div class="mb-4">
      <div class="row g-3">
        <!-- Фильтр по режиссерам -->
        <div class="col-12 col-md-4">
          <div class="dropdown">
            <button
              class="btn btn-secondary dropdown-toggle w-100"
              type="button"
              id="dropdownDirectors"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Фильтр по режиссерам
              <span v-if="selectedDirectorFilters.length > 0">
                ({{ selectedDirectorFilters.length }})
              </span>
            </button>
            <ul class="dropdown-menu p-3" aria-labelledby="dropdownDirectors" style="max-height: 250px; overflow-y: auto;">
              <li>
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="selectAllDirectors"
                    :checked="allDirectorsSelected"
                    @change="toggleAllDirectors"
                  />
                  <label class="form-check-label" for="selectAllDirectors">
                    Все режиссеры
                  </label>
                </div>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li v-for="director in directors" :key="director.id">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'director-' + director.id"
                    :value="director.id"
                    v-model="selectedDirectorFilters"
                  />
                  <label class="form-check-label" :for="'director-' + director.id">
                    {{ director.name }}
                  </label>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Фильтр по студиям -->
        <div class="col-12 col-md-4">
          <div class="dropdown">
            <button
              class="btn btn-secondary dropdown-toggle w-100"
              type="button"
              id="dropdownStudios"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Фильтр по студиям
              <span v-if="selectedStudioFilters.length > 0">
                ({{ selectedStudioFilters.length }})
              </span>
            </button>
            <ul class="dropdown-menu p-3" aria-labelledby="dropdownStudios" style="max-height: 250px; overflow-y: auto;">
              <li>
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="selectAllStudios"
                    :checked="allStudiosSelected"
                    @change="toggleAllStudios"
                  />
                  <label class="form-check-label" for="selectAllStudios">
                    Все студии
                  </label>
                </div>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li v-for="studioItem in studios" :key="studioItem.id">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'studio-' + studioItem.id"
                    :value="studioItem.id"
                    v-model="selectedStudioFilters"
                  />
                  <label class="form-check-label" :for="'studio-' + studioItem.id">
                    {{ studioItem.name }}
                  </label>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Фильтр по статусам -->
        <div class="col-12 col-md-4">
          <div class="dropdown">
            <button
              class="btn btn-secondary dropdown-toggle w-100"
              type="button"
              id="dropdownStatuses"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Фильтр по статусам
              <span v-if="selectedStatusFilters.length > 0">
                ({{ selectedStatusFilters.length }})
              </span>
            </button>
            <ul class="dropdown-menu p-3" aria-labelledby="dropdownStatuses" style="max-height: 250px; overflow-y: auto;">
              <li>
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="selectAllStatuses"
                    :checked="allStatusesSelected"
                    @change="toggleAllStatuses"
                  />
                  <label class="form-check-label" for="selectAllStatuses">
                    Все статусы
                  </label>
                </div>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li v-for="statusItem in statuses" :key="statusItem.id">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'status-' + statusItem.id"
                    :value="statusItem.id"
                    v-model="selectedStatusFilters"
                  />
                  <label class="form-check-label" :for="'status-' + statusItem.id">
                    {{ statusItem.name }}
                  </label>
                </div>
              </li>
            </ul>
          </div>
        </div>
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
              :src="getFullImageUrl(anime.picture_url) || '/media/noIMG.jpg'" 
              class="card-img-top" 
              alt="Изображение аниме" 
              style="height: 200px; object-fit: cover;"
              @contextmenu.prevent
              draggable="false"
            />
            <div class="card-body text-center">
              <h5 class="card-title">{{ anime.title_name }}</h5>
            </div>
          </router-link>

          <!-- Кнопки редактирования и удаления -->
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
      <div class="modal-dialog modal-dialog-centered">
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

              <!-- Название -->
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

              <!-- Статус, Дата -->
              <div class="row">
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

              <!-- Директор, Студия -->
              <div class="row">
                <div class="col">
                  <div class="form-floating mb-3">
                    <select 
                      class="form-select" 
                      v-model="animeToEdit.director"
                      :required="!isAnnouncementEdit"
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
                <div class="col">
                  <div class="form-floating mb-3">
                    <select 
                      class="form-select" 
                      v-model="animeToEdit.studio"
                      :required="!isAnnouncementEdit"
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
              </div>

              <!-- Жанры -->
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
                        v-for="genreId in selectedGenresEdit"
                        :key="genreId"
                        :value="genreId"
                      >
                        {{ getGenreNameById(genreId) }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Изображение -->
              <div class="row mt-3">
                <div class="col">
                  <div class="d-flex align-items-center justify-content-end">
                    <img 
                      :src="animeAddImageEditUrl || getFullImageUrl(animeToEdit.picture_url) || '/media/noIMG.jpg'" 
                      alt="Изображение" 
                      style="max-height: 60px; max-width: 60px;" 
                      v-if="animeAddImageEditUrl || animeToEdit.picture_url"
                      class="me-2"
                      @contextmenu.prevent
                      draggable="false"
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
            <img 
              :src="selectedImage" 
              class="img-fluid" 
              alt="Увеличенное изображение"
              @contextmenu.prevent
              draggable="false"
            >
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

// Изображения
const animesPictureRef = ref();
const animeAddImageUrl = ref();
const animesPictureToEditRef = ref();
const animeAddImageEditUrl = ref();

// Модальные окна
const editModal = ref(null);

// Статистика
const animeStats = ref({});

// Объявления
const isAnnouncement = computed(() => {
  const announcementStatus = statuses.value.find(s => s.name.toLowerCase() === 'анонс');
  return animeToAdd.value.status === announcementStatus?.id;
});

const isAnnouncementEdit = computed(() => {
  const announcementStatus = statuses.value.find(s => s.name.toLowerCase() === 'анонс');
  return animeToEdit.value.status === announcementStatus?.id;
});

// Фильтры
const userToFilter = ref('all');
const usersToFilter = ref([]);

// Новые фильтры: режиссеры, студии, статусы
const selectedDirectorFilters = ref([]);
const selectedStudioFilters = ref([]);
const selectedStatusFilters = ref([]);

// Проверка на выбор всех
const allDirectorsSelected = computed(() => directors.value.length > 0 && selectedDirectorFilters.value.length === directors.value.length);
const allStudiosSelected = computed(() => studios.value.length > 0 && selectedStudioFilters.value.length === studios.value.length);
const allStatusesSelected = computed(() => statuses.value.length > 0 && selectedStatusFilters.value.length === statuses.value.length);

// Вспомогательная переменная для изображения
const selectedImage = ref('');
const imageModalInstance = ref(null);

// Применение фильтров (исправлено)
async function applyFilters() {
  try {
    let url = '/api/animes/';
    const params = new URLSearchParams();

    // Фильтр по пользователю
    if (userToFilter.value) {
      if (is_superuser.value) {
        if (userToFilter.value !== 'all') {
          params.append('user', userToFilter.value);
        }
      } else if (is_staff.value) {
        if (userToFilter.value === 'my') {
          params.append('user', username.value);
        } else if (userToFilter.value === 'all') {
          params.append('user', 'all');
        }
      }
    }

    // Фильтры по режиссерам
    if (selectedDirectorFilters.value.length > 0) {
      selectedDirectorFilters.value.forEach(d_id => params.append('directors', d_id));
    }

    // Фильтры по студиям
    if (selectedStudioFilters.value.length > 0) {
      selectedStudioFilters.value.forEach(s_id => params.append('studios', s_id));
    }

    // Фильтры по статусам
    if (selectedStatusFilters.value.length > 0) {
      selectedStatusFilters.value.forEach(st_id => params.append('statuses', st_id));
    }

    const queryString = params.toString();
    if (queryString) {
      url += `?${queryString}`;
    }

    const response = await axios.get(url);
    animes.value = response.data;
    animes.value.sort((a, b) => b.id - a.id);

    await applyStatsFilters();
  } catch (error) {
    console.error('Ошибка при применении фильтров:', error);
    alert('Не удалось применить фильтры.');
  }
}

async function applyStatsFilters() {
  try {
    let url = '/api/animes/stats/';
    const params = new URLSearchParams();

    // Фильтр по пользователю
    if (userToFilter.value) {
      if (is_superuser.value) {
        if (userToFilter.value !== 'all') {
          params.append('user', userToFilter.value);
        }
      } else if (is_staff.value) {
        if (userToFilter.value === 'my') {
          params.append('user', username.value);
        } else if (userToFilter.value === 'all') {
          params.append('user', 'all');
        }
      }
    }

    // Фильтры для статистики
    if (selectedDirectorFilters.value.length > 0) {
      selectedDirectorFilters.value.forEach(d_id => params.append('directors', d_id));
    }
    if (selectedStudioFilters.value.length > 0) {
      selectedStudioFilters.value.forEach(s_id => params.append('studios', s_id));
    }
    if (selectedStatusFilters.value.length > 0) {
      selectedStatusFilters.value.forEach(st_id => params.append('statuses', st_id));
    }

    const queryString = params.toString();
    if (queryString) {
      url += `?${queryString}`;
    }

    const response = await axios.get(url);
    animeStats.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статистики с фильтрами:', error);
    alert('Не удалось загрузить статистику с учетом фильтров.');
  }
}

// Watchers
watch([selectedDirectorFilters, selectedStudioFilters, selectedStatusFilters, userToFilter], () => {
  applyFilters();
});

// Выбор всех режиссеров
function toggleAllDirectors(event) {
  if (event.target.checked) {
    selectedDirectorFilters.value = directors.value.map(d => d.id);
  } else {
    selectedDirectorFilters.value = [];
  }
}

// Выбор всех студий
function toggleAllStudios(event) {
  if (event.target.checked) {
    selectedStudioFilters.value = studios.value.map(s => s.id);
  } else {
    selectedStudioFilters.value = [];
  }
}

// Выбор всех статусов
function toggleAllStatuses(event) {
  if (event.target.checked) {
    selectedStatusFilters.value = statuses.value.map(st => st.id);
  } else {
    selectedStatusFilters.value = [];
  }
}

// Загрузка данных
async function fetchUsers() {
  try {
    const response = await axios.get('/api/animes/users/');
    usersToFilter.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке пользователей:', error);
    alert('Не удалось загрузить список пользователей.');
  }
}

async function fetchGenres() {
  try {
    const response = await axios.get('/api/genres/');
    genres.value = response.data;
    availableGenresAdd.value = [...genres.value];
    availableGenresEdit.value = [...genres.value];
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

// Обработка изображений
function animesAddPictureChange() {
  if (animesPictureRef.value.files[0]) {
    animeAddImageUrl.value = URL.createObjectURL(animesPictureRef.value.files[0]);
  } else {
    animeAddImageUrl.value = null;
  }
}

function animesAddPictureEditChange() {
  if (animesPictureToEditRef.value.files[0]) {
    animeAddImageEditUrl.value = URL.createObjectURL(animesPictureToEditRef.value.files[0]);
  } else {
    animeAddImageEditUrl.value = null;
  }
}

// CRUD аниме
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
    resetAddForm();
    applyFilters();
  } catch (error) {
    handleError(error, 'добавлении аниме');
  }
}

function resetAddForm() {
  animeToAdd.value = {
    title_name: '',
    date: '',
    studio: null,
    director: null,
    genres: [],
    status: '',
  };
  availableGenresAdd.value = [...genres.value];
  selectedGenresAdd.value = [];
  selectedAvailableGenresAdd.value = [];
  selectedSelectedGenresAdd.value = [];
  animeAddImageUrl.value = null;
  if (animesPictureRef.value) {
    animesPictureRef.value.value = '';
  }
}

function onAnimeEdit(anime) {
  animeToEdit.value = { ...anime };
  animeAddImageEditUrl.value = null;
  
  selectedGenresEdit.value = [...anime.genres];
  availableGenresEdit.value = genres.value.filter(genre => !anime.genres.includes(genre.id));
  
  selectedAvailableGenresEdit.value = [];
  selectedSelectedGenresEdit.value = [];
  
  editModal.value.show();
}

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

  selectedGenresEdit.value.forEach(genreId => {
    formData.append('genres', genreId);
  });

  if (animesPictureToEditRef.value?.files[0]) {
    formData.append('picture', animesPictureToEditRef.value.files[0]);
  } else if (animeToEdit.value.picture_url === null) {
    formData.append('picture', '');
  }

  try {
    await axios.put(`/api/animes/${animeToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    animeAddImageEditUrl.value = null;
    if (animesPictureToEditRef.value) {
      animesPictureToEditRef.value.value = '';
    }
    closeModal();
    applyFilters();
  } catch (error) {
    handleError(error, 'обновлении аниме');
  }
}

async function onAnimeDelete(id) {
  if (!confirm('Вы уверены, что хотите удалить это аниме?')) {
    return;
  }

  try {
    await axios.delete(`/api/animes/${id}/`);
    applyFilters();
  } catch (error) {
    console.error('Ошибка при удалении аниме:', error);
    alert('Не удалось удалить аниме.');
  }
}

function toggleGenresAdd() {
  if (selectedAvailableGenresAdd.value.length > 0) {
    selectedAvailableGenresAdd.value.forEach((genreId) => {
      if (!selectedGenresAdd.value.includes(genreId)) {
        selectedGenresAdd.value.push(genreId);
        availableGenresAdd.value = availableGenresAdd.value.filter(g => g.id !== genreId);
      }
    });
    selectedAvailableGenresAdd.value = [];
  } else if (selectedSelectedGenresAdd.value.length > 0) {
    selectedSelectedGenresAdd.value.forEach((genreId) => {
      availableGenresAdd.value.push(genres.value.find(g => g.id === genreId));
      selectedGenresAdd.value = selectedGenresAdd.value.filter(id => id !== genreId);
    });
    selectedSelectedGenresAdd.value = [];
  }
}

function toggleGenresEdit() {
  if (selectedAvailableGenresEdit.value.length > 0) {
    selectedAvailableGenresEdit.value.forEach((genreId) => {
      if (!selectedGenresEdit.value.includes(genreId)) {
        selectedGenresEdit.value.push(genreId);
        availableGenresEdit.value = availableGenresEdit.value.filter(g => g.id !== genreId);
      }
    });
    selectedAvailableGenresEdit.value = [];
  } else if (selectedSelectedGenresEdit.value.length > 0) {
    selectedSelectedGenresEdit.value.forEach((genreId) => {
      availableGenresEdit.value.push(genres.value.find(g => g.id === genreId));
      selectedGenresEdit.value = selectedGenresEdit.value.filter(id => id !== genreId);
    });
    selectedSelectedGenresEdit.value = [];
  }
}

// Вспомогательные функции
function getGenreNameById(genreId) {
  const genre = genres.value.find(g => g.id === genreId);
  return genre ? genre.name : 'Неизвестный жанр';
}

function getFullImageUrl(relativePath) {
  if (!relativePath) return '/media/noIMG.jpg';
  
  if (relativePath.startsWith('http://') || relativePath.startsWith('https://')) {
    return relativePath;
  }
  
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const cleanPath = relativePath.startsWith('/') ? relativePath : '/' + relativePath;
  
  return `${baseUrl}${cleanPath}`;
}

function closeModal() {
  const modalElement = document.getElementById('editAnimeModal');
  const modalInstance = Modal.getInstance(modalElement);
  modalInstance.hide();
  
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

function removePicture() {
  animeToEdit.value.picture_url = null;
  animeAddImageEditUrl.value = null;
  if (animesPictureToEditRef.value) {
    animesPictureToEditRef.value.value = '';
  }
}

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

function canEditDelete(anime) {
  return is_superuser.value || (is_staff.value && anime.username === username.value);
}

onMounted(async () => {
  await userProfileStore.fetchUserProfile();

  if (is_superuser.value) {
    await fetchUsers();
  }

  await fetchGenres();
  await fetchStudios();
  await fetchDirectors();
  await fetchStatuses();

  // Изначально выбираем все режиссеры, студии, статусы
  if (directors.value.length > 0) {
    selectedDirectorFilters.value = directors.value.map(d => d.id);
  }
  if (studios.value.length > 0) {
    selectedStudioFilters.value = studios.value.map(s => s.id);
  }
  if (statuses.value.length > 0) {
    selectedStatusFilters.value = statuses.value.map(st => st.id);
  }

  await applyFilters();

  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

  const modalElement = document.getElementById('editAnimeModal');
  editModal.value = new Modal(modalElement, {
    backdrop: 'static',
    keyboard: false,
  });

  const imageModalElement = document.getElementById('imageModal');
  imageModalInstance.value = new Modal(imageModalElement, {
    backdrop: 'static',
    keyboard: false,
  });
});
</script>

<style lang="scss" scoped>
.fixed-width {
  width: 50%; 
}

.fixed-width select {
  width: 100%;
}

.form-label {
  margin-bottom: 0.5rem;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: 0.3s;
}

.card .btn {
  background-color: rgba(255, 255, 255, 0.8);
}

.card .btn:hover {
  background-color: rgba(255, 255, 255, 1);
}

.card .btn-success {
  background-color: #28a745 !important;
  border-color: #28a745 !important;
}

.card .btn-danger {
  background-color: #dc3545 !important;
  border-color: #dc3545 !important;
}

.card-img-top {
  width: 100%;
  height: 200px;
  object-fit: cover;
  pointer-events: none;
}
</style>
