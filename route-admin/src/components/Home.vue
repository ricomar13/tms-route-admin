<template>
  <q-page class="bg-grey-1 q-pa-lg">
    <div class="row q-col-gutter-md items-center q-mb-lg">
      <div class="col">
        <h1 class="text-h4 text-weight-bold text-primary q-ma-none">Panel de Operaciones</h1>
        <p class="text-subtitle1 text-grey-7">Monitoreo de rutas activas y estado de flota</p>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card class="no-shadow bordered-purple overflow-hidden">
          <q-card-section class="q-pa-none">
            <RouteMap :selectedRoute="selectedRoute" :allRoutes="activeRoutes" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card class="no-shadow bordered-purple full-height">
          <q-card-section class="row items-center">
            <div class="text-h6 text-weight-bold text-primary">Rutas en Tránsito</div>
            <q-space />
            <q-btn 
              flat 
              round 
              icon="add_location" 
              color="primary" 
              to="/routes?action=add" 
            >
              <q-tooltip>Ir a crear nueva ruta</q-tooltip>
            </q-btn>
          </q-card-section>

          <q-list separator class="q-ma-sm" v-if="activeRoutes.length > 0">
            <q-item 
              v-for="route in activeRoutes" 
              :key="route.id" 
              clickable 
              @click="selectedRoute = route" 
              :active="selectedRoute?.id === route.id" 
              active-class="bg-purple-1 text-primary" 
              class="rounded-borders q-mb-sm border-grey"
            >
              <q-item-section avatar><q-icon name="local_shipping" :color="selectedRoute?.id === route.id ? 'primary' : 'grey-7'" /></q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ route.name }}</q-item-label>
                <q-item-label caption>{{ route.origin_name }} → {{ route.destination_name }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>

          <div v-else class="column items-center justify-center q-pa-xl text-grey-6">
            <q-icon name="map" size="64px" class="q-mb-md" />
            <div class="text-weight-bold uppercase">No hay rutas activas</div>
            <div class="text-caption text-center">Usa el botón superior para programar un nuevo viaje en el panel maestro</div>
          </div>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-md q-mt-lg">
      <div class="col-12">
        <q-card class="no-shadow bordered-purple">
          <q-card-section class="row items-center">
            <div class="text-h6 text-weight-bold text-grey-9">Estado de Unidades</div>
            <q-space />
            <q-btn flat color="primary" label="Gestionar Flota" icon="settings" to="/trucks" no-caps />
          </q-card-section>
          <q-table flat :rows="trucks" :columns="truckColumns" row-key="id" :loading="loading" :pagination="{ rowsPerPage: 5 }">
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-chip :color="getStatusColor(props.value)" text-color="white" size="sm" dense class="text-weight-bold text-uppercase">
                  {{ props.value }}
                </q-chip>
              </q-td>
            </template>
          </q-table>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api.js';
import RouteMap from './RouteMap.vue';

const routes = ref([]);
const trucks = ref([]);
const loading = ref(true);
const selectedRoute = ref(null);

const activeRoutes = computed(() => routes.value.filter(r => r.status === 'en_transito'));

const truckColumns = [
  { name: 'plate', align: 'left', label: 'PLACA', field: 'plate', sortable: true },
  { name: 'model', align: 'left', label: 'MODELO', field: 'model', sortable: true },
  { name: 'status', align: 'center', label: 'ESTADO', field: 'status', sortable: true }
];

const getStatusColor = (s) => s === 'disponible' ? 'positive' : s === 'en_ruta' ? 'primary' : 'negative';

const loadData = async () => {
  try {
    const [resR, resT] = await Promise.all([api.get('/routes'), api.get('/trucks')]);
    routes.value = resR.data;
    trucks.value = resT.data;
  } finally { loading.value = false; }
};

onMounted(loadData);
</script>

<style scoped>
.bordered-purple { border-left: 6px solid #673ab7; border-radius: 16px; background: white; }
.bg-purple-1 { background: #f3e5f5; }
.border-grey { border: 1px solid #eeeeee; }
</style>