<template>
  <div class="container mt-5">
    <h1 class="mb-4">Страны студий</h1>

    <!-- Форма для добавления новой страны -->
    <form @submit.prevent="onCountryAdd" v-if="is_auth && is_staff">
      <div class="row align-items-end">
        <!-- Поле Название страны -->
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="countryToAdd.name"
              required
              placeholder="Название страны"
            />
            <label>Название страны</label>
          </div>
        </div>
        <div class="col d-flex justify-content-end">
          <div class="col-auto me-3">
            <img 
              :src="countryAddImageUrl" 
              alt="Изображение" 
              style="max-height: 60px; max-width: 60px;" 
              v-if="countryAddImageUrl"
              @contextmenu.prevent
              draggable="false"
            />
          </div>
          <div class="col-auto me-3">
            <input 
              type="file" 
              class="form-control" 
              ref="countryPictureRef" 
              @change="countryAddPictureChange"
              accept="image/*"
            />
          </div>
          <button type="submit" class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>
    
    <!-- Блок для отображения статистики -->
    <div class="card mb-4 mt-4">
      <div class="card-body">
        <h5 class="card-title">Статистика стран</h5>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <strong>Всего стран: </strong> {{ countryStats['Всего стран:'] || 0 }}
          </li>
          <li class="list-group-item">
            <strong>Больше всего студий в: </strong> {{ countryStats['Больше всего студий в:'] || '-' }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Список стран -->
    <table class="table table-striped mt-5">
      <thead>
        <tr>
          <th>Название страны</th>
          <th class="col-2 text-center">Изображение</th>
          <th class="col-md-1" v-if="is_superuser">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="country in countries" :key="country.id">
          <td>{{ country.name }}</td>
          <td>
            <div v-if="country.picture" class="d-flex justify-content-center align-items-center">
              <img 
                :src="getFullImageUrl(country.picture)" 
                style="max-height: 60px; max-width: auto; cursor: pointer;" 
                alt="Изображение страны"
                @click="showImage(getFullImageUrl(country.picture))"
                @contextmenu.prevent
                draggable="false"
              />
            </div>
          </td>
          <td v-if="is_superuser">
            <button
              class="btn btn-success btn-sm me-2"
              @click="onCountryEdit(country)"
              title="Редактировать"
            >
              <i class="bi bi-pen-fill"></i>
            </button>
            <button
              class="btn btn-danger btn-sm"
              @click="onCountryDelete(country.id)"
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
      id="editCountryModal"
      tabindex="-1"
      aria-labelledby="editCountryModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="onCountryUpdate">
            <div class="modal-header">
              <h5 class="modal-title" id="editCountryModalLabel">
                Редактировать страну
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
                  v-model="countryToEdit.name"
                  required
                  placeholder="Название страны"
                />
                <label>Название страны</label>
              </div>
              <div class="row mt-3">
                <div class="col">
                  <div class="d-flex align-items-center justify-content-end">
                    <img 
                      :src="countryAddImageEditUrl || getFullImageUrl(countryToEdit.picture)" 
                      alt="Изображение страны" 
                      style="max-height: 60px; max-width: 60px;" 
                      v-if="countryAddImageEditUrl || countryToEdit.picture"
                      class="me-2"
                      @contextmenu.prevent
                      draggable="false"
                    />
                    <button 
                      type="button" 
                      class="btn btn-danger btn-sm me-2" 
                      @click="removePicture" 
                      v-if="countryAddImageEditUrl || countryToEdit.picture"
                      title="Удалить изображение"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                    <input 
                      type="file" 
                      class="form-control w-auto" 
                      ref="countryPictureToEditRef" 
                      @change="countryAddPictureEditChange"
                      accept="image/*"
                    />
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
const countries = ref([]);
const countryToAdd = ref({
  name: '',
  picture: null
});
const countryToEdit = ref({
  id: null,
  name: '',
  picture: null
});

// Реактивные переменные для изображений
const countryPictureRef = ref();
const countryAddImageUrl = ref();
const countryPictureToEditRef = ref();
const countryAddImageEditUrl = ref();

// Экземпляры модальных окон
const editModal = ref(null);
const imageModal = ref(null);

// Статистика стран
const countryStats = ref({});

// Вспомогательные переменные для просмотра изображения
const selectedImage = ref('');

// Функции загрузки данных с бэкенда
async function fetchCountries() {
  try {
    const response = await axios.get('/api/countries/');
    countries.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке стран:', error);
    alert('Не удалось загрузить страны.');
  }
}

async function fetchCountryStats() {
  try {
    const response = await axios.get('/api/countries/stats/');
    countryStats.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статистики стран:', error);
    alert('Не удалось загрузить статистику стран.');
  }
}

// Функция добавления новой страны
async function onCountryAdd() {
  // Проверка на существующее название
  const existingCountry = countries.value.find(
    c => c.name.toLowerCase() === countryToAdd.value.name.toLowerCase()
  );
  
  if (existingCountry) {
    alert('Страна с таким названием уже существует');
    return;
  }

  const formData = new FormData();
  formData.append('name', countryToAdd.value.name);
  
  if (countryPictureRef.value.files[0]) {
    formData.append('picture', countryPictureRef.value.files[0]);
  }

  try {
    await axios.post('/api/countries/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchCountries();
    await fetchCountryStats();
    resetAddForm();
  } catch (error) {
    handleError(error, 'добавлении страны');
  }
}

// Функция подготовки к редактированию страны
function onCountryEdit(country) {
  countryToEdit.value = { ...country };
  // Сбрасываем URL временного изображения при открытии формы редактирования
  countryAddImageEditUrl.value = null;
  
  // Показать модальное окно через Bootstrap Modal API
  editModal.value.show();
}

// Функция обновления страны
async function onCountryUpdate() {
  // Проверка на существующее название
  const existingCountry = countries.value.find(
    c => c.name.toLowerCase() === countryToEdit.value.name.toLowerCase() 
    && c.id !== countryToEdit.value.id
  );
  
  if (existingCountry) {
    alert('Страна с таким названием уже существует');
    return;
  }

  const formData = new FormData();
  formData.append('name', countryToEdit.value.name);
  
  if (countryPictureToEditRef.value?.files[0]) {
    formData.append('picture', countryPictureToEditRef.value.files[0]);
  } else if (countryToEdit.value.picture === null) {
    formData.append('picture', '');
  }

  try {
    await axios.put(`/api/countries/${countryToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchCountries();
    await fetchCountryStats();
    closeModal();
  } catch (error) {
    handleError(error, 'обновлении страны');
  }
}

// Функция удаления страны
async function onCountryDelete(id) {
  if (!confirm('Вы уверены, что хотите удалить эту страну?')) {
    return;
  }

  try {
    await axios.delete(`/api/countries/${id}/`);
    await fetchCountries();
    await fetchCountryStats();
  } catch (error) {
    console.error('Ошибка при удалении страны:', error);
    alert('Не удалось удалить страну.');
  }
}

// Функция для получения полного URL изображения
function getFullImageUrl(url) {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  return `${import.meta.env.VITE_API_URL}${url}`;
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

// Функции для обработки изображений
function countryAddPictureChange() {
  if (countryPictureRef.value.files[0]) {
    countryAddImageUrl.value = URL.createObjectURL(countryPictureRef.value.files[0]);
  } else {
    countryAddImageUrl.value = null;
  }
}

function countryAddPictureEditChange() {
  if (countryPictureToEditRef.value.files[0]) {
    countryAddImageEditUrl.value = URL.createObjectURL(countryPictureToEditRef.value.files[0]);
  } else {
    countryAddImageEditUrl.value = null;
  }
}

// Функция сброса формы добавления
function resetAddForm() {
  countryToAdd.value = {
    name: '',
    picture: null
  };
  if (countryPictureRef.value) {
    countryPictureRef.value.value = '';
  }
  countryAddImageUrl.value = null;
}

// Функция закрытия модального окна редактирования
function closeModal() {
  editModal.value.hide();

  // Очистка полей изображения
  countryAddImageEditUrl.value = null;
  if (countryPictureToEditRef.value) {
    countryPictureToEditRef.value.value = '';
  }
}

// Функция удаления изображения при редактировании
function removePicture() {
  countryToEdit.value.picture = null;
  countryAddImageEditUrl.value = null;
  if (countryPictureToEditRef.value) {
    countryPictureToEditRef.value.value = '';
  }
}

// Функция для просмотра увеличенного изображения
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

  fetchCountries();
  fetchCountryStats();
  // Установка CSRF токена
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

  // Инициализация модального окна для редактирования
  const editModalElement = document.getElementById('editCountryModal');
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
/* Здесь могут быть специфичные стили для компонента Country */
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
