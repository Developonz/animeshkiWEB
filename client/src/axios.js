import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 404) {
      console.log('Ресурс не найден')
    }
    return Promise.reject(error)
  }
);

export default axios; 