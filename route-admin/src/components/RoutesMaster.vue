<template>
  <q-page class="q-pa-md bg-grey-1">
    <div class="row items-center q-mb-md">
      <div class="text-h5 text-weight-bold text-primary">Gestión Maestra de Rutas</div>
      <q-space />
      <q-input dense outlined v-model="filter" placeholder="Buscar ruta o camión..." class="bg-white">
        <template v-slot:append><q-icon name="search" /></template>
      </q-input>
    </div>

    <q-card class="no-shadow bordered-purple">
      <q-table
        :rows="routes"
        :columns="columns"
        :filter="filter"
        flat
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-badge :color="props.value === 'completada' ? 'green' : 'orange'">
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api.js';

const routes = ref([]);
const filter = ref('');
const columns = [
  { name: 'name', label: 'NOMBRE RUTA', field: 'name', align: 'left', sortable: true },
  { name: 'origin', label: 'ORIGEN', field: 'origin_name', align: 'left' },
  { name: 'destination', label: 'DESTINO', field: 'destination_name', align: 'left' },
  { name: 'status', label: 'ESTADO', field: 'status', align: 'center' }
];

onMounted(async () => {
  const res = await api.get('/routes');
  routes.value = res.data;
});
</script>