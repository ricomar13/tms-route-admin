<template>
  <div id="map" style="height: 450px; border-radius: 12px; z-index: 1;"></div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';

const props = defineProps({ selectedRoute: Object, allRoutes: Array });

let map;
let routingControl;
const markersGroup = L.layerGroup(); // Manejador de capas para limpiar marcadores

// Configuración de Iconos para entorno Vite
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
let DefaultIcon = L.icon({ iconUrl: markerIcon, shadowUrl: markerShadow, iconSize: [25, 41], iconAnchor: [12, 41] });
L.Marker.prototype.options.icon = DefaultIcon;

const initMap = () => {
  if (map) return;
  map = L.map('map').setView([19.4326, -99.1332], 5);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap'
  }).addTo(map);
  markersGroup.addTo(map);
};

const clearMapFeatures = () => {
  markersGroup.clearLayers(); // Elimina marcadores anteriores
  if (routingControl) {
    map.removeControl(routingControl); // Elimina la línea azul anterior
    routingControl = null;
  }
};

const drawOverview = () => {
  clearMapFeatures();
  if (!props.allRoutes) return;
  props.allRoutes.forEach(r => {
    L.marker([r.origin_lat, r.origin_lng])
      .addTo(markersGroup)
      .bindPopup(`<b>${r.name}</b><br>Haz clic en la lista derecha para ver trayecto.`);
  });
};

const drawSingleRoute = (route) => {
  clearMapFeatures();
  if (!route) { drawOverview(); return; }

  // Dibujar puntos A y B reales de la ruta seleccionada
  L.marker([route.origin_lat, route.origin_lng]).addTo(markersGroup).bindPopup(`<b>Origen:</b> ${route.origin_name}`);
  L.marker([route.destination_lat, route.destination_lng]).addTo(markersGroup).bindPopup(`<b>Destino:</b> ${route.destination_name}`);

  routingControl = L.Routing.control({
    waypoints: [
      L.latLng(route.origin_lat, route.origin_lng),
      L.latLng(route.destination_lat, route.destination_lng)
    ],
    lineOptions: { styles: [{ color: '#673ab7', weight: 6, opacity: 0.8 }] },
    addWaypoints: false, draggableWaypoints: false, show: false,
    createMarker: () => null // Usamos nuestros marcadores para evitar duplicados
  }).addTo(map);

  routingControl.on('routesfound', (e) => {
    map.fitBounds(L.latLngBounds(e.routes[0].coordinates), { padding: [50, 50] });
  });
};

watch(() => props.selectedRoute, (newVal) => drawSingleRoute(newVal));
watch(() => props.allRoutes, () => drawOverview(), { deep: true });

onMounted(() => {
  initMap();
  drawOverview();
});
</script>

<style>
.leaflet-routing-container { display: none !important; }
</style>