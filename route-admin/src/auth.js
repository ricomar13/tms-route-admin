// src/auth.js
import { reactive } from 'vue';
import axios from 'axios';

export const authState = reactive({
  isAuthenticated: !!localStorage.getItem('access_token'),
  user: null,
});

// Función centralizada para loguearse
export async function login(username, password) {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  try {
    const response = await axios.post('http://127.0.0.1:8000/users/token', params);
    const token = response.data.access_token;
    
    localStorage.setItem('access_token', token);
    authState.isAuthenticated = true;
    return true; // Éxito
  } catch (error) {
    console.error('Error en auth.js login:', error);
    return false; // Fallo
  }
}

export function logout() {
  localStorage.removeItem('access_token');
  authState.isAuthenticated = false;
  authState.user = null;
}