import { createRouter, createWebHistory } from 'vue-router';
import { authState } from '../auth';
import RoutesMaster from '../components/RoutesMaster.vue';

// componentes de "página"
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
    meta: { requiresAuth: true } 
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true } 
  },
  {
    path: '/routes',
    name: 'Routes',
    component: RoutesMaster,
    meta: { requiresAuth: true }
  },
  {
    path: '/trucks',
    name: 'Trucks',
    component: () => import('../components/TrucksMaster.vue'),
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

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