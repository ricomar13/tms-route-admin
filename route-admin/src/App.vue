<script setup>
import Navbar from './components/Navbar.vue';
import { authState } from './auth.js';
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
// Doble validación: Que esté autenticado Y que no estemos en la página de login
const showNavbar = computed(() => authState.isAuthenticated && route.path !== '/login');
</script>

<template>
  <q-layout view="hHh Lpr lFf" class="bg-grey-1">
    
    <Navbar v-if="showNavbar" />

    <q-page-container>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </q-page-container>

  </q-layout>
</template>

<style>
/* Estilo para una transición suave entre pantallas */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

body {
  margin: 0;
  font-family: 'Roboto', sans-serif;
}
</style>