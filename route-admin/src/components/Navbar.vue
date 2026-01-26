<script setup>
import { logout } from '../auth.js';
import { useRouter } from 'vue-router';

const router = useRouter();

function handleLogout() {
  logout();
  router.push('/login');
}
</script>

<template>
  <q-header elevated class="bg-white text-primary q-py-xs">
    <q-toolbar>
      <q-icon name="local_shipping" size="md" class="q-mr-sm" />
      
      <q-toolbar-title class="text-weight-bolder">
        Route<span class="text-grey-8">Admin</span>
      </q-toolbar-title>

      <q-space />

      <div class="q-gutter-sm row items-center no-wrap gt-xs">
        <q-btn flat no-caps label="Inicio" to="/" icon="dashboard" class="rounded-borders" />
        
        <q-btn flat no-caps label="Mi Perfil" to="/profile" icon="account_circle" class="rounded-borders" />
        
        <q-btn 
          flat 
          no-caps 
          label="Rutas" 
          to="/routes" 
          icon="map" 
          class="rounded-borders" 
        />

        <q-separator vertical inset class="q-mx-md" />

        <q-btn 
          unelevated 
          no-caps 
          color="primary" 
          label="Cerrar Sesión" 
          icon="logout" 
          @click="handleLogout"
          class="rounded-borders q-px-md"
        />
      </div>

      <q-btn flat round dense icon="menu" class="lt-sm" />
    </q-toolbar>
  </q-header>
</template>

<style scoped>
.q-router-link--active {
  background: rgba(103, 58, 183, 0.1) !important;
  font-weight: bold;
}

.q-btn:hover {
  transform: translateY(-1px);
  transition: transform 0.2s;
}
</style>