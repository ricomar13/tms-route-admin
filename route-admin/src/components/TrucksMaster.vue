<template>
  <q-page class="q-pa-md bg-grey-1">
    <div class="row items-center q-mb-md">
      <div class="text-h5 text-weight-bold text-primary">Gestión de Flota Vehicular</div>
      <q-space />
      <q-btn color="primary" label="Registrar Unidad" icon="add" unelevated @click="openAddDialog" />
    </div>

    <q-card class="no-shadow bordered-purple">
      <q-table 
        :rows="trucks" 
        :columns="columns" 
        flat 
        row-key="id" 
        :pagination="{ rowsPerPage: 10 }"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-btn-dropdown dense unelevated :color="getStatusColor(props.value)" :label="props.value" size="sm">
              <q-list>
                <q-item clickable v-close-popup @click="handleStatusChange(props.row, 'disponible')"><q-item-section>Disponible</q-item-section></q-item>
                <q-item clickable v-close-popup @click="handleStatusChange(props.row, 'en_ruta')"><q-item-section>En Ruta</q-item-section></q-item>
                <q-item clickable v-close-popup @click="handleStatusChange(props.row, 'mantenimiento')"><q-item-section>Fuera de Servicio</q-item-section></q-item>
              </q-list>
            </q-btn-dropdown>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="q-gutter-xs text-center">
            <q-btn flat round color="primary" icon="edit" size="sm" @click="openEditDialog(props.row)" />
            <q-btn flat round color="negative" icon="delete" size="sm" @click="confirmDelete(props.row)" />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <q-dialog v-model="showDialog" persistent>
      <q-card style="min-width: 350px; border-radius: 15px">
        <q-card-section class="bg-primary text-white text-h6">{{ isEdit ? 'Editar' : 'Nueva' }} Unidad</q-card-section>
        <q-card-section class="q-gutter-md q-pt-lg">
          <q-input filled v-model="form.plate" label="Número de Placa" />
          <q-input filled v-model="form.model" label="Nombre / Modelo" />
          <q-input filled v-model.number="form.capacity" label="Capacidad (kg)" type="number" />
        </q-card-section>
        <q-card-actions class="justify-end q-pb-md q-pr-md">
          <q-btn flat label="Cancelar" v-close-popup color="grey" />
          <q-btn unelevated color="primary" label="Guardar" @click="saveTruck" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import api from '../api.js';

const $q = useQuasar();
const trucks = ref([]);
const routes = ref([]);
const showDialog = ref(false);
const isEdit = ref(false);
const form = ref({ plate: '', model: '', capacity: 0, status: 'disponible' });

const columns = [
  { name: 'plate', label: 'PLACA', field: 'plate', align: 'left', sortable: true },
  { name: 'model', label: 'MODELO', field: 'model', align: 'left', sortable: true },
  { name: 'capacity', label: 'CAPACIDAD (KG)', field: 'capacity', align: 'center', sortable: true },
  { name: 'status', label: 'ESTADO', field: 'status', align: 'center', sortable: true },
  { name: 'actions', label: 'ACCIONES', align: 'center' }
];

const loadData = async () => {
  const [resT, resR] = await Promise.all([api.get('/trucks'), api.get('/routes')]);
  trucks.value = resT.data;
  routes.value = resR.data;
};

const getStatusColor = (s) => s === 'disponible' ? 'positive' : s === 'en_ruta' ? 'primary' : 'negative';

// VALIDACIÓN DE ESTADO
async function handleStatusChange(truck, newStatus) {
  if (newStatus === 'disponible') {
    const hasActiveRoute = routes.value.some(r => r.truck_id === truck.id && r.status === 'en_transito');
    if (hasActiveRoute) {
      $q.notify({ color: 'negative', message: 'No puedes ponerlo disponible: tiene una ruta activa.', icon: 'error' });
      return;
    }
  }
  await api.patch(`/trucks/${truck.id}`, { status: newStatus });
  loadData();
}

const openAddDialog = () => { isEdit.value = false; form.value = { plate: '', model: '', capacity: 0, status: 'disponible' }; showDialog.value = true; };
const openEditDialog = (t) => { isEdit.value = true; form.value = { ...t }; showDialog.value = true; };

async function saveTruck() {
  if (isEdit.value) await api.patch(`/trucks/${form.value.id}`, form.value);
  else await api.post('/trucks/', form.value);
  showDialog.value = false;
  loadData();
}

async function confirmDelete(truck) {
  const hasActive = routes.value.some(r => r.truck_id === truck.id && r.status === 'en_transito');
  if (hasActive) {
    $q.notify({ color: 'negative', message: 'No se puede eliminar un camión en tránsito.' });
    return;
  }
  $q.dialog({ title: 'Confirmar', message: `¿Borrar unidad ${truck.plate}?`, cancel: true }).onOk(async () => {
    await api.delete(`/trucks/${truck.id}`);
    loadData();
  });
}

onMounted(loadData);
</script>

<style scoped> .bordered-purple { border-left: 6px solid #673ab7; border-radius: 12px; } </style>