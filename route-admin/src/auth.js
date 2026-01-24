// En src/auth.js

import { reactive } from 'vue';

// Este objeto será nuestro estado global.
// "reactive" significa que Vue observará cualquier cambio en él.
export const authState = reactive({
  isAuthenticated: false,
  user: null, // Aquí podríamos guardar datos del usuario más adelante
});

export function logout() {
  localStorage.removeItem('access_token');
  authState.isAuthenticated = false;
  authState.user = null;
}
// Opcional: redirigir al login si estás usando Vue Router
  // router.push('/login');

// Al cargar la app, revisamos si ya existe un token en localStorage
// para mantener al usuario logueado entre sesiones.
const token = localStorage.getItem('access_token');
if (token) {
  authState.isAuthenticated = true;
}