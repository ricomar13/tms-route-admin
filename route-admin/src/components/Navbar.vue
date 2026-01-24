<script setup>
// Importamos la función logout en lugar de la lógica directa
import { logout } from '../auth.js';
import { useRouter } from 'vue-router';

const router = useRouter(); // <-- 2. Obtén la instancia del router

function handleLogout() {
  logout(); // <-- Simplemente llamamos a la función
  router.push('/login'); // Redirige a la página de Login
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">RouteAdmin</router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Profile' }">Perfil</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" href="#">Rutas</a>
          </li>
        </ul>

        <button 
          @click="handleLogout" 
          class="btn btn-outline-danger"
        >
          Cerrar Sesión
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Estilo para que el enlace activo se vea diferente */
.router-link-exact-active {
  font-weight: bold;
  color: white !important;
}
</style>