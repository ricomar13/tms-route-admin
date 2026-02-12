<template>
  <q-page class="q-pa-md bg-grey-1">
    <div class="row items-center q-mb-md">
      <div class="text-h5 text-weight-bold text-primary">Gestión Maestra de Rutas</div>
      <q-space />
      <div class="row q-gutter-sm">
        <q-input dense outlined v-model="filter" placeholder="Buscar ruta, origen..." class="bg-white" style="min-width: 250px">
          <template v-slot:append><q-icon name="search" /></template>
        </q-input>
        <q-btn color="primary" label="Nueva Ruta" icon="add" unelevated @click="openAddDialog" />
      </div>
    </div>

    <q-card class="no-shadow bordered-purple">
      <q-table :rows="routes" :columns="columns" :filter="filter" flat row-key="id" :pagination="initialPagination">
        <template v-slot:body-cell-truck="props">
          <q-td :props="props"><q-chip icon="local_shipping" outline color="grey-8" size="sm">{{ getTruckPlate(props.row.truck_id) }}</q-chip></q-td>
        </template>
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-btn-dropdown dense unelevated :color="props.value === 'en_transito' ? 'orange' : 'green'" :label="props.value" size="sm">
              <q-list>
                <q-item clickable v-close-popup @click="updateStatus(props.row, 'en_transito')"><q-item-section>En Tránsito</q-item-section></q-item>
                <q-item clickable v-close-popup @click="updateStatus(props.row, 'terminada')"><q-item-section>Terminada</q-item-section></q-item>
              </q-list>
            </q-btn-dropdown>
          </q-td>
        </template>
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="q-gutter-xs text-center">
            <q-btn flat round color="primary" icon="edit" size="sm" @click="openEditDialog(props.row)" />
            <q-btn flat round color="negative" icon="delete" size="sm" @click="confirmDelete(props.row.id)" />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <q-dialog v-model="showDialog" persistent>
      <q-card style="min-width: 500px; border-radius: 15px">
        <q-card-section class="bg-primary text-white text-h6">
          {{ isEdit ? 'Editar Ruta' : 'Programar Nueva Ruta' }}
        </q-card-section>
        
        <q-card-section class="q-gutter-md q-pt-lg">
          <q-input filled v-model="form.name" label="Nombre de la ruta/carga" color="primary" />
          
          <q-select filled v-model="originCity" use-input input-debounce="500" label="Ciudad Origen" 
            :options="cityOptions" @filter="searchCities" @update:model-value="setOrigin" />

          <q-select filled v-model="destCity" use-input input-debounce="500" label="Ciudad Destino" 
            :options="cityOptions" @filter="searchCities" @update:model-value="setDestination" />

          <q-select filled v-model="selectedTruck" :options="trucks" option-label="plate" label="Asignar Camión"
            :option-disable="(opt) => opt.status === 'mantenimiento'" />
        </q-card-section>

        <q-card-actions class="justify-end q-pb-md q-pr-md">
          <q-btn flat label="Cancelar" v-close-popup color="grey" />
          <q-btn unelevated color="primary" :label="isEdit ? 'Guardar Cambios' : 'Activar Ruta'" @click="saveRoute" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import { useRoute, useRouter } from 'vue-router';
import api from '../api.js';

const $q = useQuasar();
const qRoute = useRoute();
const qRouter = useRouter();

const routes = ref([]);
const trucks = ref([]);
const filter = ref('');
const showDialog = ref(false);
const isEdit = ref(false);

const initialPagination = { sortBy: 'name', page: 1, rowsPerPage: 10 };
const columns = [
  { name: 'name', label: 'NOMBRE', field: 'name', align: 'left', sortable: true },
  { name: 'origin', label: 'ORIGEN', field: 'origin_name', align: 'left', sortable: true },
  { name: 'destination', label: 'DESTINO', field: 'destination_name', align: 'left', sortable: true },
  { name: 'truck', label: 'CAMIÓN', align: 'left', sortable: true },
  { name: 'status', label: 'ESTADO', field: 'status', align: 'center', sortable: true },
  { name: 'actions', label: 'ACCIONES', align: 'center' }
];

// Refs Formulario
const form = ref({ name: '', origin_name: '', origin_lat: 0, origin_lng: 0, destination_name: '', destination_lat: 0, destination_lng: 0, status: 'en_transito' });
const originCity = ref(null);
const destCity = ref(null);
const selectedTruck = ref(null);
const cityOptions = ref([]);

const loadData = async () => {
  const [resR, resT] = await Promise.all([api.get('/routes'), api.get('/trucks')]);
  routes.value = resR.data;
  trucks.value = resT.data;
};

const getTruckPlate = (id) => trucks.value.find(t => t.id === id)?.plate || 'N/A';

// Lógica Geocoding
async function searchCities(val, update) {
  if (val.length < 3) { update(() => cityOptions.value = []); return; }
  const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${val}&countrycodes=mx`);
  const data = await res.json();
  update(() => cityOptions.value = data.map(i => ({ label: i.display_name, name: i.name, lat: parseFloat(i.lat), lng: parseFloat(i.lon) })));
}

const setOrigin = (v) => { if (v) { form.value.origin_name = v.name; form.value.origin_lat = v.lat; form.value.origin_lng = v.lng; } };
const setDestination = (v) => { if (v) { form.value.destination_name = v.name; form.value.destination_lat = v.lat; form.value.destination_lng = v.lng; } };

// Abrir Modales
const openAddDialog = () => {
  isEdit.value = false;
  form.value = { name: '', origin_name: '', origin_lat: 0, origin_lng: 0, destination_name: '', destination_lat: 0, destination_lng: 0, status: 'en_transito' };
  originCity.value = null; destCity.value = null; selectedTruck.value = null;
  showDialog.value = true;
};

const openEditDialog = (r) => {
  isEdit.value = true;
  form.value = { ...r };
  originCity.value = r.origin_name;
  destCity.value = r.destination_name;
  selectedTruck.value = trucks.value.find(t => t.id === r.truck_id);
  showDialog.value = true;
};

// Guardar/Actualizar
async function saveRoute() {
  try {
    const payload = { ...form.value, truck_id: selectedTruck.value.id };
    if (isEdit.value) {
      await api.patch(`/routes/${form.value.id}`, payload);
    } else {
      await api.post('/routes', payload);
      await api.patch(`/trucks/${selectedTruck.value.id}`, { status: 'en_ruta' });
    }
    showDialog.value = false;
    loadData();
    $q.notify({ color: 'positive', message: 'Operación exitosa' });
  } catch (e) { $q.notify({ color: 'negative', message: 'Error en el servidor' }); }
}

async function updateStatus(route, newStatus) {
  await api.patch(`/routes/${route.id}`, { status: newStatus });
  loadData();
}

const confirmDelete = (id) => { $q.dialog({ title: 'Borrar', message: '¿Eliminar ruta?', cancel: true }).onOk(async () => { await api.delete(`/routes/${id}`); loadData(); }); };

onMounted(async () => {
  await loadData();
  // LÓGICA DE REDIRECCIÓN DESDE INICIO
  if (qRoute.query.action === 'add') {
    openAddDialog();
    // Limpiar la URL para que no se abra de nuevo al refrescar
    qRouter.replace({ query: null });
  }
});
</script>

<style scoped> .bordered-purple { border-left: 6px solid #673ab7; border-radius: 12px; } </style>