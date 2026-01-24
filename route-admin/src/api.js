import axios from 'axios';
import { logout } from './auth.js';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  // Si la respuesta es exitosa (código 2xx), simplemente la devuelve.
  (response) => response,

  // Si la respuesta es un error...
  (error) => {
    // Si el error es un 401 (No Autorizado)...
    if (error.response && error.response.status === 401) {
      // ...ejecuta la función de logout.
      logout();
    }
    // Devuelve el error para que el componente que hizo la llamada también lo sepa.
    return Promise.reject(error);
  }
);

export default api;