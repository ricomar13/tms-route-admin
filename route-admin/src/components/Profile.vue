<template>
  <q-page class="bg-grey-1 q-pa-md flex flex-center">
    <q-card class="profile-card no-shadow">
      
      <q-card-section class="bg-primary text-white q-pb-xl" style="height: 120px">
        <div class="text-h6 text-weight-bold">
          {{ isEditing ? 'Editando Perfil' : 'Perfil de Usuario' }}
        </div>
      </q-card-section>

      <q-card-section class="text-center q-pa-none" style="margin-top: -50px">
        <q-avatar size="100px" class="bg-white shadow-5">
          <q-icon :name="isEditing ? 'edit_note' : 'person'" color="primary" size="60px" />
        </q-avatar>
      </q-card-section>

      <q-card-section v-if="!user && !error" class="text-center">
        <q-spinner-dots color="primary" size="40px" />
        <p>Cargando datos de MariaDB...</p>
      </q-card-section>

      <q-card-section v-else-if="error" class="text-center">
        <q-icon name="error" color="negative" size="lg" />
        <div class="text-negative">{{ error }}</div>
      </q-card-section>

      <template v-else-if="user && !isEditing">
        <q-card-section class="q-pt-md">
          <div class="text-center q-mb-lg">
            <div class="text-h5 text-weight-bolder text-grey-9">{{ user.full_name }}</div>
            <q-badge color="secondary" :label="user.role || 'Usuario'" class="q-pa-xs" />
          </div>

          <q-list padding>
            <q-item>
              <q-item-section avatar><q-icon name="badge" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label caption>Código de Empleado</q-item-label>
                <q-item-label class="text-weight-bold">{{ user.user_code }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section avatar><q-icon name="alternate_email" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label caption>Correo Corporativo</q-item-label>
                <q-item-label class="text-weight-bold">{{ user.email }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section avatar><q-icon name="account_circle" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label caption>Nombre de Usuario</q-item-label>
                <q-item-label class="text-weight-bold">@{{ user.username }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>

        <q-separator inset />
        <q-card-actions class="justify-center q-pb-lg">
          <q-btn flat color="primary" icon="edit" label="Editar Datos" @click="startEditing" no-caps />
          <q-btn flat color="grey-7" icon="lock_reset" label="Seguridad" no-caps />
        </q-card-actions>
      </template>

      <q-form v-else-if="isEditing" @submit.prevent="handleUpdate">
        <q-card-section class="q-gutter-sm q-px-xl">
          <div class="row q-col-gutter-sm">
            <div class="col-12 col-sm-6"><q-input filled dense v-model="editData.first_name" label="Nombre" /></div>
            <div class="col-12 col-sm-6"><q-input filled dense v-model="editData.last_name" label="Apellido" /></div>
          </div>
          <q-input filled dense v-model="editData.email" label="Email" type="email" />
          <q-input filled dense v-model="editData.username" label="Username" />
          <q-input filled dense v-model="editData.password" label="Nueva Contraseña" type="password" hint="Opcional" />
        </q-card-section>

        <q-card-actions class="justify-center q-pb-lg q-px-xl">
          <q-btn label="Guardar" type="submit" color="primary" class="full-width rounded-borders" />
          <q-btn flat label="Cancelar" color="grey-7" @click="isEditing = false" class="full-width q-mt-sm" />
        </q-card-actions>
      </q-form>

    </q-card>
  </q-page>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import api from '../api.js'; // Usamos tu archivo api.js con el token
import { useQuasar } from 'quasar';

const $q = useQuasar();
const user = ref(null);
const error = ref(null);
const isEditing = ref(false);

const editData = reactive({
  username: '', email: '', first_name: '', middle_name: '',
  last_name: '', second_last_name: '', password: ''
});

// Cargar datos
onMounted(async () => {
  try {
    const response = await api.get('/users/me');
    user.value = response.data;
  } catch (err) {
    error.value = 'Error al conectar con MariaDB.';
    console.error(err);
  }
});

function startEditing() {
  Object.assign(editData, user.value);
  editData.password = '';
  isEditing.value = true;
}

async function handleUpdate() {
  try {
    const updatePayload = {};
    for (const key in editData) {
      if (editData[key]) updatePayload[key] = editData[key];
    }

    const response = await api.patch('/users/me', updatePayload);
    user.value = response.data;
    isEditing.value = false;

    $q.notify({
      color: 'positive', icon: 'check_circle', message: '¡Perfil actualizado!', position: 'top'
    });
  } catch (err) {
    $q.notify({
      color: 'negative', icon: 'report_problem', message: 'Error al actualizar', position: 'top'
    });
  }
}
</script>

<style scoped>
.profile-card {
  width: 100%;
  max-width: 500px;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid #e0e0e0;
  background: white;
}
</style>