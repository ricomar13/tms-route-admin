<template>
  <q-page class="bg-grey-1 q-pa-md flex flex-center">
    <q-card class="profile-card no-shadow border-purple-thin">
      
      <q-card-section class="bg-primary text-white q-pb-xl" style="height: 120px; border-radius: 0 0 40px 40px">
        <div class="row items-center no-wrap">
          <div class="col">
            <div class="text-h6 text-weight-bold">
              {{ isEditing ? 'Actualizar Perfil' : 'Mi Perfil' }}
            </div>
            <div class="text-caption">Gestión de cuenta administrativa</div>
          </div>
          <q-icon :name="isEditing ? 'edit_square' : 'verified_user'" size="md" opacity="0.5" />
        </div>
      </q-card-section>

      <q-card-section class="text-center q-pa-none" style="margin-top: -50px">
        <q-avatar size="100px" class="bg-white shadow-10">
          <q-icon :name="isEditing ? 'manage_accounts' : 'person'" color="primary" size="60px" />
        </q-avatar>
      </q-card-section>

      <q-card-section v-if="loading" class="text-center q-pa-xl">
        <q-spinner-ios color="primary" size="40px" />
        <p class="text-grey-7 q-mt-md">Sincronizando datos...</p>
      </q-card-section>

      <template v-else-if="user && !isEditing">
        <q-card-section class="q-pt-md">
          <div class="text-center q-mb-lg">
            <div class="text-h5 text-weight-bolder text-grey-9">
              {{ user.first_name }} {{ user.last_name }}
            </div>
            <q-badge color="purple-2" text-color="primary" :label="user.role" class="q-pa-xs text-weight-bold" />
          </div>

          <q-list padding class="text-grey-9">
            <q-item clickable v-ripple class="rounded-borders">
              <q-item-section avatar><q-icon name="alternate_email" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label caption>Correo Corporativo</q-item-label>
                <q-item-label class="text-weight-medium">{{ user.email }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple class="rounded-borders">
              <q-item-section avatar><q-icon name="badge" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label caption>Código de Empleado</q-item-label>
                <q-item-label class="text-weight-medium">{{ user.user_code }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple class="rounded-borders">
              <q-item-section avatar><q-icon name="account_circle" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label caption>Nombre de Usuario</q-item-label>
                <q-item-label class="text-weight-medium">@{{ user.username }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>

        <q-separator inset class="q-my-sm" />
        <q-card-actions class="justify-center q-pb-lg">
          <q-btn flat color="primary" icon="edit" label="Editar mis datos" @click="startEditing" no-caps class="rounded-borders" />
        </q-card-actions>
      </template>

      <q-form v-else-if="isEditing" @submit.prevent="handleUpdate">
        <q-card-section class="q-gutter-y-md q-px-lg q-pt-lg">
          
          <div class="text-subtitle2 text-primary text-weight-bold">Información Personal</div>
          
          <div class="row q-col-gutter-sm">
            <div class="col-6">
              <q-input filled dense v-model="editData.first_name" label="Primer Nombre" color="primary" />
            </div>
            <div class="col-6">
              <q-input filled dense v-model="editData.middle_name" label="Segundo Nombre" color="primary" />
            </div>
            <div class="col-6">
              <q-input filled dense v-model="editData.last_name" label="Primer Apellido" color="primary" />
            </div>
            <div class="col-6">
              <q-input filled dense v-model="editData.second_last_name" label="Segundo Apellido" color="primary" />
            </div>
          </div>

          <q-input filled dense v-model="editData.email" label="Email" type="email" icon="email" />
          <q-input filled dense v-model="editData.username" label="Username" />
          
          <q-separator class="q-my-sm" />
          
          <div class="text-subtitle2 text-orange-9 text-weight-bold">Seguridad (Opcional)</div>
          <q-input filled dense v-model="editData.password" label="Nueva Contraseña" type="password" />
          <q-input 
            filled dense 
            v-model="confirmPassword" 
            label="Confirmar Nueva Contraseña" 
            type="password" 
            :rules="[val => !editData.password || val === editData.password || 'Las contraseñas no coinciden']"
            lazy-rules
          />
        </q-card-section>

        <q-card-actions class="justify-center q-pb-lg q-px-lg">
          <q-btn label="Guardar Cambios" type="submit" color="primary" class="full-width rounded-borders" unelevated size="md" />
          <q-btn flat label="Cancelar" color="grey-7" @click="isEditing = false" class="full-width q-mt-xs" no-caps />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import api from '../api.js';
import { logout } from '../auth.js';

const $q = useQuasar();
const router = useRouter();

const user = ref(null);
const loading = ref(true);
const isEditing = ref(false);
const confirmPassword = ref('');

// Objeto reactivo para el formulario
const editData = reactive({
  username: '', 
  email: '', 
  first_name: '', 
  middle_name: '', 
  last_name: '', 
  second_last_name: '', 
  password: ''
});

// Función para cargar datos desde el Backend
const loadProfile = async () => {
  try {
    loading.value = true;
    const res = await api.get('/users/me');
    user.value = res.data;
  } catch (e) {
    $q.notify({ color: 'negative', message: 'Sesión expirada' });
    logout();
    router.push('/login');
  } finally {
    loading.value = false;
  }
};

onMounted(loadProfile);

// FUNCIÓN CLAVE: Pre-completa el formulario con los datos actuales
function startEditing() {
  editData.username = user.value.username;
  editData.email = user.value.email;
  editData.first_name = user.value.first_name;
  editData.middle_name = user.value.middle_name || '';
  editData.last_name = user.value.last_name;
  editData.second_last_name = user.value.second_last_name || '';
  
  // Limpiamos campos de password por seguridad
  editData.password = '';
  confirmPassword.value = '';
  
  isEditing.value = true;
}

async function handleUpdate() {
  try {
    const payload = {};
    // Solo enviamos los campos que tengan contenido
    for (const key in editData) {
      if (editData[key] !== '' && editData[key] !== null) {
        payload[key] = editData[key];
      }
    }

    await api.patch('/users/me', payload);

    if (payload.password) {
      $q.notify({ color: 'warning', message: 'Contraseña cambiada. Por seguridad, inicia sesión nuevamente.', icon: 'lock' });
      setTimeout(() => { logout(); router.push('/login'); }, 2000);
    } else {
      $q.notify({ color: 'positive', message: 'Perfil actualizado con éxito', icon: 'done' });
      isEditing.value = false;
      loadProfile(); // Refrescar vista de lectura
    }
  } catch (err) {
    const errorMsg = err.response?.data?.detail || 'Error al actualizar datos';
    $q.notify({ color: 'negative', message: errorMsg, icon: 'error' });
  }
}
</script>

<style scoped>
.profile-card {
  width: 100%;
  max-width: 480px;
  border-radius: 24px;
  background: white;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.border-purple-thin {
  border: 1px solid rgba(103, 58, 183, 0.1);
}
</style>