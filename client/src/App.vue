<template>
  <div class="container mt-5">
    <h1 class="mb-4">Аниме</h1>

    <!-- Форма для добавления нового аниме -->
    <form @submit.prevent="onAnimeAdd">
      <!-- Строка полей (кроме жанров) -->
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
              :required="isDateRequired(animeToAdd.status)"
              placeholder="Дата выпуска"
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
              :required="isFieldRequired(animeToAdd.status)"
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
              :required="isFieldRequired(animeToAdd.status)"
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

      <!-- Вторая строка полей (жанры и кнопка Добавить) -->
      <div class="row align-items-end mt-3">
        <!-- Поле Жанры с двумя списками и одной кнопкой -->
        <div class="col">
          <label>Жанры</label>
          <div class="d-flex">
            <div class="flex-fill">
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
            <div class="d-flex flex-column justify-content-center mx-2">
              <button
                type="button"
                class="btn btn-secondary"
                @click="toggleGenresAdd"
              >
                ↔
              </button>
            </div>
            <div class="flex-fill">
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

        <!-- Кнопка Добавить -->
        <div class="col-auto">
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
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="anime in animes" :key="anime.id">
          <td>{{ anime.title_name }}</td>
          <td>{{ anime.date }}</td>
          <td>{{ getStudioName(anime.studio) }}</td>
          <td>{{ getDirectorName(anime.director) }}</td>
          <td>{{ getGenreNames(anime.genres).join(', ') }}</td>
          <td>{{ getStatusName(anime.status) }}</td>
          <td>
            <button
              class="btn btn-success btn-sm me-2"
              @click="onAnimeEdit(anime)"
              data-bs-toggle="modal"
              data-bs-target="#editAnimeModal"
            >
              <i class="bi bi-pen-fill"></i>
            </button>
            <button
              class="btn btn-danger btn-sm"
              @click="onAnimeDelete(anime.id)"
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
              <!-- Поле Название -->
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

              <!-- Строка с Дата выпуска и Студия -->
              <div class="row">
                <!-- Поле Дата выпуска -->
                <div class="col">
                  <div class="form-floating mb-3">
                    <input
                      type="date"
                      class="form-control"
                      v-model="animeToEdit.date"
                      :required="isDateRequired(animeToEdit.status)"
                      placeholder="Дата выпуска"
                    />
                    <label>Дата выпуска</label>
                  </div>
                </div>

                <!-- Поле Студия -->
                <div class="col">
                  <div class="form-floating mb-3">
                    <select
                      class="form-select"
                      v-model="animeToEdit.studio"
                      :required="isFieldRequired(animeToEdit.status)"
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

              <!-- Строка с Директор и Статус -->
              <div class="row">
                <!-- Поле Директор -->
                <div class="col">
                  <div class="form-floating mb-3">
                    <select
                      class="form-select"
                      v-model="animeToEdit.director"
                      :required="isFieldRequired(animeToEdit.status)"
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

                <!-- Поле Статус -->
                <div class="col">
                  <div class="form-floating mb-3">
                    <select
                      class="form-select"
                      v-model="animeToEdit.status"
                      required
                    >
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
              </div>

              <!-- Поле Жанры с двумя списками и одной кнопкой -->
              <div class="form-group mb-3">
                <label>Жанры</label>
                <div class="d-flex">
                  <div class="flex-fill">
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
                  <div class="d-flex flex-column justify-content-center mx-2">
                    <button
                      type="button"
                      class="btn btn-secondary"
                      @click="toggleGenresEdit"
                    >
                      ↔
                    </button>
                  </div>
                  <div class="flex-fill">
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
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
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
import * as bootstrap from 'bootstrap';

// Установка CSRF токена
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

// Реактивные переменные
const animes = ref([]);
const animeToAdd = ref({
  title_name: '',
  date: '',
  studio: null,
  director: null,
  genres: [],
  status: null,
});
const animeToEdit = ref({});
const genres = ref([]);
const studios = ref([]);
const directors = ref([]);
const statuses = ref([]);

// Для поля жанров в добавлении
const availableGenresAdd = ref([]);
const selectedGenresAdd = ref([]);
const selectedAvailableGenresAdd = ref([]);
const selectedSelectedGenresAdd = ref([]);

// Для поля жанров в редактировании
const availableGenresEdit = ref([]);
const selectedGenresEdit = ref([]);
const selectedAvailableGenresEdit = ref([]);
const selectedSelectedGenresEdit = ref([]);

// Функции загрузки данных с бэкенда
async function fetchAnimes() {
  const response = await axios.get('/api/animes/');
  animes.value = response.data.map(anime => ({
    ...anime,
    date: anime.date ? new Date(anime.date).toISOString().split('T')[0] : null
  }));
}

async function fetchGenres() {
  const response = await axios.get('/api/genres/');
  genres.value = response.data;
  availableGenresAdd.value = [...genres.value];
}

async function fetchStudios() {
  const response = await axios.get('/api/studios/');
  studios.value = response.data;
}

async function fetchDirectors() {
  const response = await axios.get('/api/directors/');
  directors.value = response.data;
}

async function fetchStatuses() {
  const response = await axios.get('/api/statuses/');
  statuses.value = response.data;
  // Устанавливаем статус по умолчанию в "Вышел"
  const defaultStatus = statuses.value.find(status => status.name === 'Вышел');
  if (defaultStatus) {
    animeToAdd.value.status = defaultStatus.id;
  }
}

// Функция для определения обязательности полей
function isFieldRequired(statusId) {
  const status = statuses.value.find((status) => status.id === statusId);
  return status && status.name !== 'Анонс';
}

function isDateRequired(statusId) {
  return isFieldRequired(statusId);
}

// Функция добавления нового аниме
async function onAnimeAdd() {
  // Проверка обязательности поля статус
  if (!animeToAdd.value.status) {
    alert('Поле "Статус" обязательно для заполнения.');
    return;
  }

  // Получаем название статуса
  const selectedStatus = statuses.value.find(
    (status) => status.id === animeToAdd.value.status
  );

  // Если статус не "Анонс", проверяем обязательные поля
  if (selectedStatus.name !== 'Анонс') {
    if (
      !animeToAdd.value.director ||
      !animeToAdd.value.date ||
      !animeToAdd.value.studio
    ) {
      alert(
        'Поля "Директор", "Дата выпуска" и "Студия" обязательны для заполнения.'
      );
      return;
    }
  }

  animeToAdd.value.genres = selectedGenresAdd.value.map((g) => g.id);

  const formattedAnime = {
    ...animeToAdd.value,
    date: animeToAdd.value.date
      ? new Date(animeToAdd.value.date).toISOString().split('T')[0]
      : null,
  };

  try {
    await axios.post('/api/animes/', formattedAnime);
    await fetchAnimes();
    // Сброс формы
    animeToAdd.value = {
      title_name: '',
      date: '',
      studio: null,
      director: null,
      genres: [],
      status: animeToAdd.value.status, // Сохраняем статус по умолчанию
    };
    availableGenresAdd.value = [...genres.value];
    selectedGenresAdd.value = [];
    selectedAvailableGenresAdd.value = [];
    selectedSelectedGenresAdd.value = [];
  } catch (error) {
    // Обработка ошибок с сервера
    if (error.response && error.response.data) {
      const errorMessages = [];
      for (const [field, messages] of Object.entries(error.response.data)) {
        errorMessages.push(`${field}: ${messages.join(', ')}`);
      }
      alert(`Ошибка при добавлении аниме:\n${errorMessages.join('\n')}`);
    } else {
      console.error(error);
      alert('Произошла неизвестная ошибка при добавлении аниме.');
    }
  }
}

// Функция подготовки к редактированию аниме
function onAnimeEdit(anime) {
  animeToEdit.value = { ...anime };
  selectedGenresEdit.value = genres.value.filter((genre) =>
    anime.genres.includes(genre.id)
  );
  availableGenresEdit.value = genres.value.filter(
    (genre) => !anime.genres.includes(genre.id)
  );
  selectedAvailableGenresEdit.value = [];
  selectedSelectedGenresEdit.value = [];
}

// Функция обновления аниме
async function onAnimeUpdate() {
  // Проверка обязательности поля статус
  if (!animeToEdit.value.status) {
    alert('Поле "Статус" обязательно для заполнения.');
    return;
  }

  // Получаем название статуса
  const selectedStatus = statuses.value.find(
    (status) => status.id === animeToEdit.value.status
  );

  // Если статус не "Анонс", проверяем обязательные поля
  if (selectedStatus.name !== 'Анонс') {
    if (
      !animeToEdit.value.director ||
      !animeToEdit.value.date ||
      !animeToEdit.value.studio
    ) {
      alert(
        'Поля "Директор", "Дата выпуска" и "Студия" обязательны для заполнения.'
      );
      return;
    }
  }

  animeToEdit.value.genres = selectedGenresEdit.value.map((g) => g.id);

  const formattedAnime = {
    ...animeToEdit.value,
    date: animeToEdit.value.date
      ? new Date(animeToEdit.value.date).toISOString().split('T')[0]
      : null,
  };

  try {
    await axios.put(`/api/animes/${animeToEdit.value.id}/`, formattedAnime);
    await fetchAnimes();
    // Закрыть модальное окно после успешного обновления
    const modalElement = document.getElementById('editAnimeModal');
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
  } catch (error) {
    // Обработка ошибок с сервера
    if (error.response && error.response.data) {
      const errorMessages = [];
      for (const [field, messages] of Object.entries(error.response.data)) {
        errorMessages.push(`${field}: ${messages.join(', ')}`);
      }
      alert(`Ошибка при обновлении аниме:\n${errorMessages.join('\n')}`);
    } else {
      console.error(error);
      alert('Произошла неизвестная ошибка при обновлении аниме.');
    }
  }
}

// Функция удаления аниме
async function onAnimeDelete(id) {
  await axios.delete(`/api/animes/${id}/`);
  await fetchAnimes();
}

// Функции для управления жанрами в добавлении
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

// Функции для управления жанрами в редактировании
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

// Вспомогательные функции для отображения имен
function getGenreNames(genreIds) {
  return genres.value
    .filter((genre) => genreIds.includes(genre.id))
    .map((genre) => genre.name);
}

function getStudioName(studioId) {
  const studio = studios.value.find((studio) => studio.id === studioId);
  return studio ? studio.name : '';
}

function getDirectorName(directorId) {
  const director = directors.value.find(
    (director) => director.id === directorId
  );
  return director ? director.name : '';
}

function getStatusName(statusId) {
  const status = statuses.value.find((status) => status.id === statusId);
  return status ? status.name : '';
}

// Загрузка данных при монтировании компонента
onMounted(() => {
  fetchAnimes();
  fetchGenres();
  fetchStudios();
  fetchDirectors();
  fetchStatuses();
});
</script>

<style>
/* Стили для модального окна */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
}

.modal-dialog {
  margin-top: 10%;
}
</style>
