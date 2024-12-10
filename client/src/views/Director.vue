<template>
    <div class="container mt-5">
      <h1 class="mb-4">режиссеры</h1>
  
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
              <img :src="directorAddImageUrl" alt="Изображение" style="max-height: 60px; max-width: 60px;" v-if="directorAddImageUrl"/>
            </div>
            <div class="col-auto me-3">
              <input type="file" class="form-control" ref="directorPictureRef" @change="directorAddPictureChange"/>
            </div>
            <button type="submit" class="btn btn-primary">
              Добавить
            </button>
          </div>
        </div>
      </form>

      <div class="card mb-4 mt-4">
        <div class="card-body">
          <h5 class="card-title">Статистика режиссеров</h5>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <strong>Всего режиссеров: </strong> {{ directorStats['Всего режиссёров:'] || 0 }}
            </li>
            <li class="list-group-item">
              <strong>Самый опытный режиссер: </strong> {{ directorStats['Самый опытный режиссер:'] || 0 }}
            </li>
          </ul>
        </div>
      </div>
  
      <!-- Список директоров -->
      <table class="table table-striped mt-5">
        <thead>
          <tr>
            <th>Имя режиссера</th>
            <th class="col-2 text-center">Изображение</th>
            <th class="col-md-1">Действия</th>
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
                />
              </div>
            </td>
            <td>
              <button
                class="btn btn-success btn-sm me-2"
                @click="onDirectorEdit(director)"
                data-bs-toggle="modal"
                data-bs-target="#editDirectorModal"
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
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="onDirectorUpdate">
              <div class="modal-header">
                <h5 class="modal-title" id="editDirectorModalLabel">
                  Редактировать режиссера
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
                        :src="directorAddImageEditUrl || directorToEdit.picture" 
                        alt="Изображение" 
                        style="max-height: 60px; max-width: 60px;" 
                        v-if="directorAddImageEditUrl || directorToEdit.picture"
                        class="me-2"
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
                      <input type="file" class="form-control w-auto" ref="directorPictureToEditRef" @change="directorAddPictureEditChange"/>
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
  });
  
  // Экземпляр модального окна
  const editModal = ref(null);
  
  // Реактивные переменные для изображений
  const directorPictureRef = ref();
  const directorAddImageUrl = ref();
  const directorPictureToEditRef = ref();
  const directorAddImageEditUrl = ref();

  const directorStats = ref({});

  async function fetchDirectorStats() {
  try {
    const response = await axios.get('/api/directors/stats/');
    directorStats.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статистики аниме:', error);
    alert('Не удалось загрузить статистику аниме.');
  }
}
  
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
      resetAddForm();
    } catch (error) {
      if (error.response?.status !== 201) { // Игнорируем успешное создание
        handleError(error, 'добавлении режиссера');
      }
    }
  }
  
  // Функция подготовки к редактированию режиссера
  function onDirectorEdit(director) {
    directorToEdit.value = { ...director };
    // Показать модальное окно после подготовки данных
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
      // Очищаем поле с картинкой после успешного обновления
      directorAddImageEditUrl.value = null;
      if (directorPictureToEditRef.value) {
        directorPictureToEditRef.value.value = '';
      }
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
    directorAddImageUrl.value = URL.createObjectURL(directorPictureRef.value.files[0]);
  }

  function directorAddPictureEditChange() {
    directorAddImageEditUrl.value = URL.createObjectURL(directorPictureToEditRef.value.files[0]);
  }

  // Функция для получения полного URL изображения
  function getFullImageUrl(url) {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `${import.meta.env.VITE_API_URL}${url}`;
  }
  
  // Загрузка данных при монтировании компонента
  onMounted(() => {
    userProfileStore.fetchUserProfile();
    
    fetchDirectors();
    // Установка CSRF токена
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  
    // Инициализация модального окна
    const modalElement = document.getElementById('editDirectorModal');
    editModal.value = new Modal(modalElement, {
      backdrop: 'static', // Не закрывать при клике на backdrop
      keyboard: false, // Не закрывать при нажатии клавиши Esc
    });

    fetchDirectorStats();
  
    // Инициализация модального окна для изображения
    imageModal.value = new Modal(document.getElementById('imageModal'));
  });

  // Добавить функцию resetAddForm
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

  // Изменить функцию closeModal
  function closeModal() {
    const modalElement = document.getElementById('editDirectorModal');
    const modalInstance = Modal.getInstance(modalElement);
    modalInstance.hide();
    
    // Очистка полей изображения
    directorAddImageEditUrl.value = null;
    if (directorPictureToEditRef.value) {
      directorPictureToEditRef.value.value = '';
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
    directorToEdit.value.picture = null;
    directorAddImageEditUrl.value = null;
    if (directorPictureToEditRef.value) {
      directorPictureToEditRef.value.value = '';
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
    <style scoped>
  /* Дополнительные стили при необходимости */
  </style>
  
