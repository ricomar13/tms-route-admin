// En src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import { authState } from '../auth';

// Importa tus componentes de "página"
import Login from '../components/Login.vue';
import Profile from '../components/Profile.vue';
import Home from '../components/Home.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true } // Esta ruta requiere autenticación
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true } // Esta ruta también
  },
  // Aquí añadiremos la ruta para "Rutas" más adelante
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// "Guardia de Navegación" - Se ejecuta antes de cada cambio de ruta
router.beforeEach((to, from, next) => {
  // Si la ruta requiere autenticación Y el usuario NO está logueado...
  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    // ...lo redirigimos al login.
    next({ name: 'Login' });
  } else {
    // Si no, dejamos que continúe.
    next();
  }
});

export default router;