<template>
  <q-page class="bg-gradient-purple flex flex-center">
    <q-card class="login-card no-shadow q-pa-lg">
      
      <q-card-section class="text-center q-pt-lg">
        <q-icon name="local_shipping" color="primary" size="80px" class="q-mb-sm" />
        <div class="text-h4 text-weight-bolder text-primary">
          Route<span class="text-grey-9">Admin</span>
        </div>
        <div class="text-subtitle2 text-grey-7 q-mt-xs">Gestión Inteligente de Transporte</div>
      </q-card-section>

      <q-card-section class="q-gutter-md q-pt-xl">
        <q-input 
          filled 
          v-model="username" 
          label="Usuario" 
          color="primary"
          class="rounded-borders"
        >
          <template v-slot:prepend>
            <q-icon name="person" color="primary" />
          </template>
        </q-input>

        <q-input 
          filled 
          v-model="password" 
          type="password" 
          label="Contraseña" 
          color="primary"
          @keyup.enter="handleLogin"
        >
          <template v-slot:prepend>
            <q-icon name="lock" color="primary" />
          </template>
        </q-input>

        <q-banner v-if="errorMessage" inline-actions class="text-white bg-red rounded-borders">
          {{ errorMessage }}
        </q-banner>
      </q-card-section>

      <q-card-section class="q-pt-lg">
        <q-btn 
          unelevated 
          color="primary" 
          size="lg" 
          class="full-width text-weight-bold rounded-borders q-py-sm" 
          label="ENTRAR AL SISTEMA" 
          :loading="loading"
          @click="handleLogin"
        />
      </q-card-section>

      <q-card-section class="text-center q-pb-lg">
        <p class="text-caption text-grey-5">v1.0.0 &copy; 2026 TMS Solutions</p>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import { login } from '../auth.js'; // Ahora sí encontrará el export llamado 'login'
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');

async function handleLogin() {
  errorMessage.value = '';
  if (!username.value || !password.value) {
    errorMessage.value = 'Por favor escribe tus credenciales';
    return;
  }

  loading.value = true;
  const success = await login(username.value, password.value);
  
  if (success) {
    router.push('/');
  } else {
    errorMessage.value = 'Usuario o contraseña incorrectos';
  }
  loading.value = false;
}
</script>

<style scoped>
.bg-gradient-purple {
  background: linear-gradient(135deg, #f5f5f5 0%, #ede7f6 100%);
  min-height: 100vh;
}
.login-card {
  width: 100%;
  max-width: 450px;
  border-radius: 24px;
  background: white;
  box-shadow: 0 20px 50px rgba(103, 58, 183, 0.1) !important;
}
</style>