<script setup>
import { ref, onMounted, reactive } from 'vue';
import api from '../api.js';
import { useQuasar } from 'quasar'; // Importa el hook de Quasar para notificaciones

const $q = useQuasar(); // Obtiene el objeto de Quasar

const user = ref(null);
const error = ref(null);
const isEditing = ref(false); // Nueva variable para controlar el modo de edición

// Objeto reactivo para guardar los datos del formulario de edición
const editData = reactive({
  username: '',
  email: '',
  first_name: '',
  middle_name: '',
  last_name: '',
  second_last_name: '',
  password: '', // Campo para la nueva contraseña
});

// Carga los datos del usuario al montar el componente
onMounted(async () => {
  try {
    const response = await api.get('/users/me');
    user.value = response.data;
  } catch (err) {
    error.value = 'No se pudieron cargar los datos del perfil.';
    console.error(err);
  }
});

// Función para entrar en modo edición
function startEditing() {
  // Copia los datos actuales del usuario al formulario
  Object.assign(editData, user.value);
  editData.password = ''; // Limpia el campo de la contraseña
  isEditing.value = true;
}

// Función para guardar los cambios
async function handleUpdate() {
  try {
    // Solo enviamos los campos que tienen un valor.
    // Creamos un objeto limpio para enviar a la API.
    const updatePayload = {};
    for (const key in editData) {
      if (editData[key]) { // Si el campo no está vacío
        updatePayload[key] = editData[key];
      }
    }

    // Llama al endpoint PATCH /users/me
    const response = await api.patch('/users/me', updatePayload);
    
    // Actualiza los datos del usuario con la respuesta de la API
    user.value = response.data;
    isEditing.value = false; // Vuelve al modo de visualización

    // Muestra una notificación de éxito
    $q.notify({
      color: 'positive',
      position: 'top',
      message: 'Perfil actualizado con éxito',
      icon: 'check_circle'
    });

  } catch (err) {
    console.error('Error al actualizar:', err);
    $q.notify({
      color: 'negative',
      position: 'top',
      message: 'Error al actualizar el perfil',
      icon: 'report_problem'
    });
  }
}
</script>

<template>
  <div class="q-pa-md" style="max-width: 500px; margin: auto;">
    <h2 class="text-h5 q-mb-md">Mi Perfil</h2>

    <q-card v-if="!isEditing && user" flat bordered>
      <q-card-section>
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Nombre Completo:</strong> {{ user.full_name }}</p>
        <p><strong>User Code:</strong> {{ user.user_code }}</p>
        <p><strong>Rol:</strong> {{ user.role }}</p>
      </q-card-section>
      <q-separator />
      <q-card-actions>
        <q-btn flat color="primary" @click="startEditing">Editar Perfil</q-btn>
      </q-card-actions>
    </q-card>
    
    <q-card v-else-if="isEditing" flat bordered>
      <q-form @submit.prevent="handleUpdate">
        <q-card-section class="q-gutter-md">
          <q-input filled v-model="editData.username" label="Username" />
          <q-input filled v-model="editData.email" label="Email" type="email" />
          <q-input filled v-model="editData.first_name" label="Primer Nombre" />
          <q-input filled v-model="editData.middle_name" label="Segundo Nombre" />
          <q-input filled v-model="editData.last_name" label="Primer Apellido" />
          <q-input filled v-model="editData.second_last_name" label="Segundo Apellido" />
          <q-input filled v-model="editData.password" label="Nueva Contraseña (dejar en blanco para no cambiar)" type="password" />
        </q-card-section>
        <q-separator />
        <q-card-actions>
          <q-btn label="Guardar Cambios" type="submit" color="primary"/>
          <q-btn flat label="Cancelar" @click="isEditing = false" />
        </q-card-actions>
      </q-form>
    </q-card>

    <div v-else-if="error" class="text-red-500">
      {{ error }}
    </div>
    <div v-else>
      <q-spinner-dots color="primary" size="40px" />
      Cargando perfil...
    </div>
  </div>
</template>