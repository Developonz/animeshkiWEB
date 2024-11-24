<template>
    <div class="container mt-5">
      <h1 class="mb-4">Страны студий</h1>
  
      <!-- Форма для добавления новой страны -->
      <form @submit.prevent="onCountryAdd">
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
              <img :src="countryAddImageUrl" alt="Изображение" style="max-height: 60px; max-width: 60px;" v-if="countryAddImageUrl"/>
            </div>
            <div class="col-auto me-3">
              <input type="file" class="form-control" ref="countryPictureRef" @change="countryAddPictureChange"/>
            </div>
            <button type="submit" class="btn btn-primary">
              Добавить
            </button>
          </div>
        </div>
      </form>
  
      <!-- Список стран -->
      <table class="table table-striped mt-5">
        <thead>
          <tr>
            <th>Название страны</th>
            <th class="col-2 text-center">Изображение</th>
            <th class="col-md-1">Действия</th>
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
                />
              </div>
            </td>
            <td>
              <button
                class="btn btn-success btn-sm me-2"
                @click="onCountryEdit(country)"
                data-bs-toggle="modal"
                data-bs-target="#editCountryModal"
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
        data-bs-backdrop="static"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="onCountryUpdate">
              <div class="modal-header">
                <h5 class="modal-title" id="editCountryModalLabel">
                  Редактировать страну
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
                        :src="countryAddImageEditUrl || countryToEdit.picture" 
                        alt="Изображение" 
                        style="max-height: 60px; max-width: 60px;" 
                        v-if="countryAddImageEditUrl || countryToEdit.picture"
                        class="me-2"
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
                      <input type="file" class="form-control w-auto" ref="countryPictureToEditRef" @change="countryAddPictureEditChange"/>
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
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import Cookies from 'js-cookie';
  import { Modal } from 'bootstrap';
  
  // Реактивные переменные
  const countries = ref([]);
  const countryToAdd = ref({
    name: '',
    picture: null
  });
  const countryToEdit = ref({
    id: null,
    name: '',
  });
  
  // Экземпляр модального окна
  const editModal = ref(null);
  
  // Реактивные переменные для изображений
  const countryPictureRef = ref();
  const countryAddImageUrl = ref();
  const countryPictureToEditRef = ref();
  const countryAddImageEditUrl = ref();
  
  // Методы для обработки изображений
  function countryAddPictureChange() {
    countryAddImageUrl.value = URL.createObjectURL(countryPictureRef.value.files[0]);
  }
  
  function countryAddPictureEditChange() {
    countryAddImageEditUrl.value = URL.createObjectURL(countryPictureToEditRef.value.files[0]);
  }
  
  // Функция для получения полного URL изображения
  function getFullImageUrl(url) {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `${import.meta.env.VITE_API_URL}${url}`;
  }
  
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
      resetAddForm();
    } catch (error) {
      if (error.response?.status !== 201) { // Игнорируем успешное создание
        handleError(error, 'добавлении страны');
      }
    }
  }
  
  // Функция подготовки к редактированию страны
  function onCountryEdit(country) {
    countryToEdit.value = { ...country };
    // Показать модальное окно осле подготовки данных
    editModal.value.show();
  }
  
  // Функция обновления страны
  async function onCountryUpdate() {
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
      
      // Очищаем поле с картинкой после успешного обновления
      countryAddImageEditUrl.value = null;
      if (countryPictureToEditRef.value) {
        countryPictureToEditRef.value.value = '';
      }
      
      // Используем атрибут для закрытия
      const modalElement = document.getElementById('editCountryModal');
      const closeBtn = modalElement.querySelector('[data-bs-dismiss="modal"]');
      closeBtn.click();
      
    } catch (error) {
      handleError(error, 'обновлени страны');
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
    } catch (error) {
      console.error('Ошибка при удалении страны:', error);
      alert('Не удалось удалить страну.');
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
    fetchCountries();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  
    const modalElement = document.getElementById('editCountryModal');
    editModal.value = new Modal(modalElement, {
      backdrop: 'static'
    });
  
    // Добавьте обработчик события закрытия модального окна
    modalElement.addEventListener('hidden.bs.modal', () => {
      const backdrops = document.querySelectorAll('.modal-backdrop');
      backdrops.forEach(backdrop => backdrop.remove());
      document.body.classList.remove('modal-open');
      document.body.style.removeProperty('overflow');
      document.body.style.removeProperty('padding-right');
    });
  
    imageModal.value = new Modal(document.getElementById('imageModal'));
  });
  
  // Добавить функцию resetAddForm
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
  
  // Добавить функцию removePicture
  function removePicture() {
    countryToEdit.value.picture = null;
    countryAddImageEditUrl.value = null;
    if (countryPictureToEditRef.value) {
      countryPictureToEditRef.value.value = '';
    }
  }
  
  // Добавить функцию showImage
  const selectedImage = ref('');
  const imageModal = ref(null);
  
  function showImage(imageUrl) {
    selectedImage.value = imageUrl;
    const modal = new Modal(document.getElementById('imageModal'));
    modal.show();
  }
  </script>
  
  <style scoped>
  /* Здесь могут быть специфичные стили для компонента Country */
  </style>
  