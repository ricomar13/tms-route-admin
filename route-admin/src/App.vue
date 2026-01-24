<script setup>
import Login from './components/Login.vue';
import Profile from './components/Profile.vue';
import Navbar from './components/Navbar.vue';
import { authState } from './auth.js';
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <Navbar v-if="authState.isAuthenticated" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style>
/* Por ahora, podemos quitar los estilos 'scoped' para que Quasar funcione mejor globalmente */
</style>