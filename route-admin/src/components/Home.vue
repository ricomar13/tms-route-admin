<template>
  <q-page class="bg-grey-1 q-pa-lg">
    <div class="row q-col-gutter-md items-center q-mb-lg">
      <div class="col">
        <h1 class="text-h4 text-weight-bold text-primary q-ma-none">Panel de Operaciones</h1>
        <p class="text-subtitle1 text-grey-7">Selecciona una ruta para ver su trayecto real</p>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card class="no-shadow bordered-purple overflow-hidden">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6 text-weight-bold">Mapa de Seguimiento</div>
            <q-space />
            <q-chip v-if="selectedRoute" color="primary" text-color="white" icon="route">
              Viendo: {{ selectedRoute.name }}
            </q-chip>
          </q-card-section>
          
          <q-card-section class="q-pa-none">
            <RouteMap :selectedRoute="selectedRoute" :allRoutes="routes" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card class="no-shadow bordered-purple full-height">
          <q-card-section class="row items-center">
            <div class="text-h6 text-weight-bold">Rutas Activas</div>
            <q-space />
            <q-btn flat round icon="add_location" color="primary" @click="showRouteDialog = true" />
          </q-card-section>

          <q-list separator class="q-ma-sm">
            <q-item 
              v-for="route in routes" 
              :key="route.id" 
              clickable 
              v-ripple
              @click="selectedRoute = route"
              :active="selectedRoute?.id === route.id"
              active-class="bg-purple-1 text-primary"
              class="rounded-borders q-mb-sm border-grey"
            >
              <q-item-section avatar>
                <q-icon name="local_shipping" :color="selectedRoute?.id === route.id ? 'primary' : 'grey-7'" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ route.name }}</q-item-label>
                <q-item-label caption>{{ route.origin_name }} → {{ route.destination_name }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-icon name="chevron_right" />
              </q-item-section>
            </q-item>
            
            <q-item v-if="routes.length === 0">
              <q-item-section class="text-center text-grey-6">No hay rutas activas</q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-md q-mt-lg">
      <div class="col-12">
        <q-card class="no-shadow bordered-purple">
          <q-card-section class="row items-center">
            <div class="text-h6 text-weight-bold">Estado de la Flota</div>
            <q-space />
            <q-btn color="primary" label="Nueva Unidad" icon="add" no-caps unelevated @click="showTruckDialog = true" />
          </q-card-section>
          
          <q-table flat :rows="trucks" :columns="truckColumns" row-key="id" :loading="loading">
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-chip :color="props.value === 'disponible' ? 'positive' : 'primary'" text-color="white" size="sm" dense>
                  {{ props.value }}
                </q-chip>
              </q-td>
            </template>
          </q-table>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="showRouteDialog" persistent>
      <q-card style="min-width: 450px">
        <q-card-section class="bg-primary text-white text-h6">Nueva Ruta</q-card-section>
        <q-card-section class="q-gutter-sm">
          <q-input filled v-model="newRoute.name" label="Nombre de la ruta" />
          <div class="row q-col-gutter-sm">
            <q-input class="col-6" filled v-model="newRoute.origin_name" label="Ciudad Origen" />
            <q-input class="col-3" filled v-model.number="newRoute.origin_lat" label="Lat" type="number" step="any" />
            <q-input class="col-3" filled v-model.number="newRoute.origin_lng" label="Lng" type="number" step="any" />
          </div>
          <div class="row q-col-gutter-sm">
            <q-input class="col-6" filled v-model="newRoute.destination_name" label="Ciudad Destino" />
            <q-input class="col-3" filled v-model.number="newRoute.destination_lat" label="Lat" type="number" step="any" />
            <q-input class="col-3" filled v-model.number="newRoute.destination_lng" label="Lng" type="number" step="any" />
          </div>
          <q-select filled v-model="selectedTruck" :options="trucks" option-label="plate" label="Asignar Camión" />
        </q-card-section>
        <q-card-actions class="justify-end">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn color="primary" label="Guardar Ruta" @click="saveRoute" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import api from '../api.js';
import RouteMap from './RouteMap.vue';

const $q = useQuasar();
const routes = ref([]);
const trucks = ref([]);
const loading = ref(true);
const selectedRoute = ref(null);
const showRouteDialog = ref(false);
const showTruckDialog = ref(false);
const selectedTruck = ref(null);

const newRoute = ref({
  name: '', origin_name: '', origin_lat: 19.43, origin_lng: -99.13,
  destination_name: '', destination_lat: 20.65, destination_lng: -103.34,
  status: 'en_transito'
});

const truckColumns = [
  { name: 'plate', align: 'left', label: 'PLACA', field: 'plate' },
  { name: 'model', align: 'left', label: 'MODELO', field: 'model' },
  { name: 'status', align: 'center', label: 'ESTADO', field: 'status' }
];

const loadData = async () => {
  try {
    const [resRoutes, resTrucks] = await Promise.all([
      api.get('/routes'),
      api.get('/trucks')
    ]);
    routes.value = resRoutes.data;
    trucks.value = resTrucks.data;
  } finally { loading.value = false; }
};

onMounted(loadData);

async function saveRoute() {
  if (!selectedTruck.value || !newRoute.value.origin_name) {
    $q.notify({ color: 'warning', message: 'Datos incompletos' });
    return;
  }
  try {
    const payload = { ...newRoute.value, truck_id: selectedTruck.value.id };
    await api.post('/routes', payload);
    showRouteDialog.value = false;
    $q.notify({ color: 'positive', message: 'Ruta activa' });
    loadData(); // Recarga los datos sin refrescar toda la página
  } catch (e) { $q.notify({ color: 'negative', message: 'Error al guardar' }); }
}
</script>

<style scoped>
.bordered-purple { border-left: 6px solid #673ab7; border-radius: 16px; background: white; }
.bg-purple-1 { background: #f3e5f5; }
.border-grey { border: 1px solid #eeeeee; }
</style>