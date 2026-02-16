// src/auth.js
import { reactive } from 'vue';
import axios from 'axios';

export const authState = reactive({
  isAuthenticated: !!localStorage.getItem('access_token'),
  user: null,
});

// Función para iniciar sesión
export async function login(username, password) {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  try {
    // CAMBIO: Localhost para consistencia total
    const response = await axios.post('http://localhost:8000/users/token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    
    const token = response.data.access_token;
    localStorage.setItem('access_token', token);
    authState.isAuthenticated = true;
    return true; 
  } catch (error) {
    console.error('Error en login:', error);
    return false;
  }
}


export function logout() {
  localStorage.removeItem('access_token');
  authState.isAuthenticated = false;
  authState.user = null;
}