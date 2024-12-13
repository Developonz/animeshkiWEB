<template>
  <div class="container mt-5">
    <h1 class="mb-4">Студии</h1>

    <!-- Форма для добавления новой студии -->
    <form @submit.prevent="onStudioAdd" v-if="is_auth && is_staff">
      <div class="row align-items-end">
        <!-- Поле Название студии -->
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="studioToAdd.name"
              required
              placeholder="Название студии"
            />
            <label>Название студии</label>
          </div>
        </div>

        <!-- Поле Страна -->
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="studioToAdd.country">
              <option :value="null">Не выбрано</option>
              <option
                v-for="country in countries"
                :key="country.id"
                :value="country.id"
              >
                {{ country.name }}
              </option>
            </select>
            <label>Страна</label>
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
        <h5 class="card-title">Статистика студий</h5>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <strong>Всего студий: </strong> {{ studioStats['Всего студий:'] || 0 }}
          </li>
          <li class="list-group-item">
            <strong>Наиболее продуктивная студия: </strong> {{ studioStats['Наиболее продуктивная студия:'] || '-' }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Список студий -->
    <table class="table table-striped mt-5">
      <thead>
        <tr>
          <th>Название студии</th>
          <th class="col-md-2">Страна</th>
          <th class="col-md-1" v-if="is_superuser">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="studio in studios" :key="studio.id">
          <td>{{ studio.name }}</td>
          <td>{{ getCountryName(studio.country) }}</td>
          <td v-if="is_superuser">
            <button
              class="btn btn-success btn-sm me-2"
              @click="onStudioEdit(studio)"
              title="Редактировать"
            >
              <i class="bi bi-pen-fill"></i>
            </button>
            <button
              class="btn btn-danger btn-sm"
              @click="onStudioDelete(studio.id)"
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
      id="editStudioModal"
      tabindex="-1"
      aria-labelledby="editStudioModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="onStudioUpdate">
            <div class="modal-header">
              <h5 class="modal-title" id="editStudioModalLabel">
                Редактировать студию
              </h5>
              <button
                type="button"
                class="btn-close"
                @click="closeModal"
                aria-label="Закрыть"
              ></button>
            </div>
            <div class="modal-body">
              <!-- Поле Название студии -->
              <div class="form-floating mb-3">
                <input
                  type="text"
                  class="form-control"
                  v-model="studioToEdit.name"
                  required
                  placeholder="Название студии"
                />
                <label>Название студии</label>
              </div>

              <!-- Поле Страна -->
              <div class="form-floating mb-3">
                <select class="form-select" v-model="studioToEdit.country">
                  <option :value="null">Не выбрано</option>
                  <option
                    v-for="country in countries"
                    :key="country.id"
                    :value="country.id"
                  >
                    {{ country.name }}
                  </option>
                </select>
                <label>Страна</label>
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

    <!-- Модальное окно для просмотра изображения (если требуется) -->
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
const studios = ref([]);
const countries = ref([]);
const studioToAdd = ref({
  name: '',
  country: null,
});
const studioToEdit = ref({
  id: null,
  name: '',
  country: null,
});

// Экземпляры модальных окон
const editModal = ref(null);
const imageModal = ref(null);

// Статистика студий
const studioStats = ref({});

// Вспомогательные переменные для просмотра изображения
const selectedImage = ref('');

// Функции загрузки данных с бэкенда
async function fetchStudios() {
  try {
    const response = await axios.get('/api/studios/');
    studios.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке студий:', error);
    alert('Не удалось загрузить студии.');
  }
}

async function fetchCountries() {
  try {
    const response = await axios.get('/api/countries/');
    countries.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке стран:', error);
    alert('Не удалось загрузить страны.');
  }
}

async function fetchStudioStats() {
  try {
    const response = await axios.get('/api/studios/stats/');
    studioStats.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статистики студий:', error);
    alert('Не удалось загрузить статистику студий.');
  }
}

// Функция добавления новой студии
async function onStudioAdd() {
  try {
    await axios.post('/api/studios/', studioToAdd.value);
    await fetchStudios();
    await fetchStudioStats();
    resetAddForm();
  } catch (error) {
    handleError(error, 'добавлении студии');
  }
}

// Функция подготовки к редактированию студии
function onStudioEdit(studio) {
  studioToEdit.value = { ...studio };
  // Показать модальное окно через Bootstrap Modal API
  editModal.value.show();
}

// Функция обновления студии
async function onStudioUpdate() {
  const payload = {
    name: studioToEdit.value.name,
    country: studioToEdit.value.country,
  };

  try {
    await axios.put(`/api/studios/${studioToEdit.value.id}/`, payload);
    await fetchStudios();
    await fetchStudioStats();
    closeModal();
  } catch (error) {
    handleError(error, 'обновлении студии');
  }
}

// Функция удаления студии
async function onStudioDelete(id) {
  if (!confirm('Вы уверены, что хотите удалить эту студию?')) {
    return;
  }

  try {
    await axios.delete(`/api/studios/${id}/`);
    await fetchStudios();
    await fetchStudioStats();
  } catch (error) {
    console.error('Ошибка при удалении студии:', error);
    alert('Не удалось удалить студию.');
  }
}

// Вспомогательная функция для отображения имени страны
function getCountryName(countryId) {
  const country = countries.value.find((country) => country.id === countryId);
  return country ? country.name : 'Не выбрано';
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

// Функция сброса формы добавления
function resetAddForm() {
  studioToAdd.value = {
    name: '',
    country: null,
  };
}

// Функция закрытия модального окна редактирования
function closeModal() {
  editModal.value.hide();
}

// Функция для просмотра увеличенного изображения (если требуется)
function showImage(imageUrl) {
  selectedImage.value = imageUrl;
  imageModal.value.show();
}

// Функция закрытия модального окна просмотра изображения
function closeImageModal() {
  imageModal.value.hide();
}

// Инициализация модальных окон и загрузка данных при монтировании компонента
onMounted(() => {
  userProfileStore.fetchUserProfile();

  fetchStudios();
  fetchCountries();
  // Установка CSRF токена
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  fetchStudioStats();

  // Инициализация модального окна для редактирования
  const editModalElement = document.getElementById('editStudioModal');
  editModal.value = new Modal(editModalElement, {
    backdrop: 'static', // Не закрывать при клике на backdrop
    keyboard: false, // Не закрывать при нажатии клавиши Esc
  });

  // Инициализация модального окна для просмотра изображения (если необходимо)
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
