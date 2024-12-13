<template>
  <div class="container mt-5">
    <h1 class="mb-4">Режиссеры</h1>

    <!-- Форма для добавления нового режиссера -->
    <form @submit.prevent="onDirectorAdd" v-if="is_auth && is_staff">
      <div class="row align-items-end">
        <!-- Поле Имя режиссера -->
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="directorToAdd.name"
              required
              placeholder="Имя режиссера"
            />
            <label>Имя режиссера</label>
          </div>
        </div>
        <div class="col d-flex justify-content-end">
          <div class="col-auto me-3">
            <img 
              :src="directorAddImageUrl" 
              alt="Изображение" 
              style="max-height: 60px; max-width: 60px;" 
              v-if="directorAddImageUrl"
              @contextmenu.prevent
              draggable="false"
            />
          </div>
          <div class="col-auto me-3">
            <input 
              type="file" 
              class="form-control" 
              ref="directorPictureRef" 
              @change="directorAddPictureChange"
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
        <h5 class="card-title">Статистика режиссеров</h5>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <strong>Всего режиссеров: </strong> {{ directorStats['Всего режиссёров:'] || 0 }}
          </li>
          <li class="list-group-item">
            <strong>Самый опытный режиссер: </strong> {{ directorStats['Самый опытный режиссер:'] || 'Неизвестно' }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Список режиссеров -->
    <table class="table table-striped mt-5">
      <thead>
        <tr>
          <th>Имя режиссера</th>
          <th class="col-2 text-center">Изображение</th>
          <th class="col-md-1" v-if="is_superuser">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="director in directors" :key="director.id">
          <td>{{ director.name }}</td>
          <td>
            <div v-if="director.picture" class="d-flex justify-content-center align-items-center">
              <img 
                :src="getFullImageUrl(director.picture)" 
                style="max-height: 60px; max-width: auto; cursor: pointer;" 
                alt="Изображение режиссера"
                @click="showImage(getFullImageUrl(director.picture))"
                @contextmenu.prevent
                draggable="false"
              />
            </div>
          </td>
          <td v-if="is_superuser">
            <button
              class="btn btn-success btn-sm me-2"
              @click="onDirectorEdit(director)"
              title="Редактировать"
            >
              <i class="bi bi-pen-fill"></i>
            </button>
            <button
              class="btn btn-danger btn-sm"
              @click="onDirectorDelete(director.id)"
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
      id="editDirectorModal"
      tabindex="-1"
      aria-labelledby="editDirectorModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="onDirectorUpdate">
            <div class="modal-header">
              <h5 class="modal-title" id="editDirectorModalLabel">
                Редактировать режиссера
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
                  v-model="directorToEdit.name"
                  required
                  placeholder="Имя режиссера"
                />
                <label>Имя режиссера</label>
              </div>
              <div class="row mt-3">
                <div class="col">
                  <div class="d-flex align-items-center justify-content-end">
                    <img 
                      :src="directorAddImageEditUrl || getFullImageUrl(directorToEdit.picture)" 
                      alt="Изображение" 
                      style="max-height: 60px; max-width: 60px;" 
                      v-if="directorAddImageEditUrl || directorToEdit.picture"
                      class="me-2"
                      @contextmenu.prevent
                      draggable="false"
                    />
                    <button 
                      type="button" 
                      class="btn btn-danger btn-sm me-2" 
                      @click="removePicture" 
                      v-if="directorAddImageEditUrl || directorToEdit.picture"
                      title="Удалить изображение"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                    <input 
                      type="file" 
                      class="form-control w-auto" 
                      ref="directorPictureToEditRef" 
                      @change="directorAddPictureEditChange"
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
const directors = ref([]);
const directorToAdd = ref({
  name: '',
  picture: null
});
const directorToEdit = ref({
  id: null,
  name: '',
  picture: null
});

// Реактивные переменные для изображений
const directorPictureRef = ref();
const directorAddImageUrl = ref();
const directorPictureToEditRef = ref();
const directorAddImageEditUrl = ref();

// Экземпляры модальных окон
const editModal = ref(null);

// Статистика режиссеров
const directorStats = ref({});

// Вспомогательные переменные для просмотра изображения
const selectedImage = ref('');
const imageModal = ref(null);

// Функции загрузки данных с бэкенда
async function fetchDirectors() {
  try {
    const response = await axios.get('/api/directors/');
    directors.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке режиссеров:', error);
    alert('Не удалось загрузить режиссеров.');
  }
}

async function fetchDirectorStats() {
  try {
    let url = '/api/directors/stats/';
    
    if (is_superuser.value || is_staff.value) {
      // Если необходимы фильтры, добавьте их здесь аналогично anime.vue
      // Например, если есть фильтр по пользователям, добавьте параметры запроса
    }
    
    const response = await axios.get(url);
    directorStats.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статистики режиссеров:', error);
    alert('Не удалось загрузить статистику режиссеров.');
  }
}

// Функция добавления нового режиссера
async function onDirectorAdd() {
  const formData = new FormData();
  formData.append('name', directorToAdd.value.name);
  
  if (directorPictureRef.value.files[0]) {
    formData.append('picture', directorPictureRef.value.files[0]);
  }

  try {
    await axios.post('/api/directors/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchDirectors();
    await fetchDirectorStats();
    resetAddForm();
  } catch (error) {
    handleError(error, 'добавлении режиссера');
  }
}

// Функция подготовки к редактированию режиссера
function onDirectorEdit(director) {
  directorToEdit.value = { ...director };
  // Сбрасываем URL временного изображения при открытии формы редактирования
  directorAddImageEditUrl.value = null;
  
  // Показать модальное окно через Bootstrap Modal API
  editModal.value.show();
}

// Функция обновления режиссера
async function onDirectorUpdate() {
  const formData = new FormData();
  formData.append('name', directorToEdit.value.name);
  
  if (directorPictureToEditRef.value?.files[0]) {
    formData.append('picture', directorPictureToEditRef.value.files[0]);
  } else if (directorToEdit.value.picture === null) {
    formData.append('picture', '');
  }

  try {
    await axios.put(`/api/directors/${directorToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchDirectors();
    await fetchDirectorStats();
    closeModal();
  } catch (error) {
    handleError(error, 'обновлении режиссера');
  }
}

// Функция удаления режиссера
async function onDirectorDelete(id) {
  if (!confirm('Вы уверены, что хотите удалить этого режиссера?')) {
    return;
  }

  try {
    await axios.delete(`/api/directors/${id}/`);
    await fetchDirectors();
    await fetchDirectorStats();
  } catch (error) {
    console.error('Ошибка при удалении режиссера:', error);
    alert('Не удалось удалить режиссера.');
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

// Методы для обработки изображений
function directorAddPictureChange() {
  if (directorPictureRef.value.files[0]) {
    directorAddImageUrl.value = URL.createObjectURL(directorPictureRef.value.files[0]);
  } else {
    directorAddImageUrl.value = null;
  }
}

function directorAddPictureEditChange() {
  if (directorPictureToEditRef.value.files[0]) {
    directorAddImageEditUrl.value = URL.createObjectURL(directorPictureToEditRef.value.files[0]);
  } else {
    directorAddImageEditUrl.value = null;
  }
}

// Функция для получения полного URL изображения
function getFullImageUrl(url) {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  return `${import.meta.env.VITE_API_URL}${url}`;
}

// Функция сброса формы добавления
function resetAddForm() {
  directorToAdd.value = {
    name: '',
    picture: null
  };
  if (directorPictureRef.value) {
    directorPictureRef.value.value = '';
  }
  directorAddImageUrl.value = null;
}

// Функция закрытия модального окна редактирования
function closeModal() {
  editModal.value.hide();
  
  // Очистка полей изображения
  directorAddImageEditUrl.value = null;
  if (directorPictureToEditRef.value) {
    directorPictureToEditRef.value.value = '';
  }
}

// Функция удаления изображения при редактировании
function removePicture() {
  directorToEdit.value.picture = null;
  directorAddImageEditUrl.value = null;
  if (directorPictureToEditRef.value) {
    directorPictureToEditRef.value.value = '';
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
  
  fetchDirectors();
  fetchDirectorStats();
  // Установка CSRF токена
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

  // Инициализация модального окна для редактирования
  const editModalElement = document.getElementById('editDirectorModal');
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
