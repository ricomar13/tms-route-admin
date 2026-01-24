<script setup>
import { ref } from 'vue';
import axios from 'axios';
// Import estado de autenticación
import { authState } from '../auth.js';
import { useRouter } from 'vue-router'; // <-- 1. Importa useRouter

const router = useRouter(); // <-- 2. Obtén la instancia del router
const username = ref('');
const password = ref('');
const errorMessage = ref('');

async function handleLogin() {
  console.log("¡Botón presionado! La función handleLogin se ha iniciado.");
  errorMessage.value = '';
  const params = new URLSearchParams();
  params.append('username', username.value);
  params.append('password', password.value);

  try {
    const response = await axios.post('http://127.0.0.1:8000/users/token', params);
    const token = response.data.access_token;
    
    // Guarda el token en localStorage.
    localStorage.setItem('access_token', token);
    
    // Actualiza estado global user autenticado.
    authState.isAuthenticated = true;
    
    alert('¡Login exitoso!');
    router.push('/'); // Redirige a la página Home

  } catch (error) {
    console.error('Error en el login:', error.response.data);
    errorMessage.value = 'El nombre de usuario o la contraseña son incorrectos.';
  }
}
</script>

<template>
  <div class="q-pa-md" style="max-width: 400px; margin: auto;">
    <h2 class="text-h6 q-mb-md">Iniciar Sesión</h2>
    
    <q-form @submit.prevent="handleLogin" class="q-gutter-md">
      
      <q-input
        filled
        v-model="username"
        label="Usuario *"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Por favor, escribe tu usuario']"
      >
        <template v-slot:prepend>
          <q-icon name="person" />
        </template>
      </q-input>

      <q-input
        filled
        type="password"
        v-model="password"
        label="Contraseña *"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Por favor, escribe tu contraseña']"
      >
        <template v-slot:prepend>
          <q-icon name="lock" />
        </template>
      </q-input>

      <q-banner v-if="errorMessage" inline-actions class="text-white bg-red">
        {{ errorMessage }}
      </q-banner>

      <div>
        <q-btn label="Entrar" type="submit" color="primary" class="full-width"/>
      </div>
    </q-form>
  </div>
</template>