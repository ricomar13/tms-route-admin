<template>
  <div id="map" style="height: 450px; border-radius: 12px; z-index: 1;"></div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';

// Props para recibir la ruta a dibujar
const props = defineProps({
  selectedRoute: Object,
  allRoutes: Array
});

let map;
let routingControl;
const markers = ref([]);

// Configuración de Iconos para Vite
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
};

const drawAllMarkers = () => {
  // Limpiar marcadores viejos
  markers.value.forEach(m => map.removeLayer(m));
  markers.value = [];

  if (!props.allRoutes) return;

  props.allRoutes.forEach(route => {
    const m = L.marker([route.origin_lat, route.origin_lng])
      .addTo(map)
      .bindPopup(`<b>${route.name}</b><br>Origen: ${route.origin_name}`);
    markers.value.push(m);
  });
};

const drawSelectedRoute = (route) => {
  // Eliminar ruta anterior si existe
  if (routingControl) {
    map.removeControl(routingControl);
  }

  if (!route) return;

  routingControl = L.Routing.control({
    waypoints: [
      L.latLng(route.origin_lat, route.origin_lng),
      L.latLng(route.destination_lat, route.destination_lng)
    ],
    lineOptions: {
      styles: [{ color: '#673ab7', weight: 6, opacity: 0.8 }]
    },
    addWaypoints: false,
    draggableWaypoints: false,
    show: false, // Oculta el panel de texto
    createMarker: () => null // No duplicar marcadores
  }).addTo(map);

  // Zoom a la ruta seleccionada
  routingControl.on('routesfound', (e) => {
    const bounds = L.latLngBounds(e.routes[0].coordinates);
    map.fitBounds(bounds, { padding: [50, 50] });
  });
};

// Observar cuando cambia la ruta seleccionada en el Home
watch(() => props.selectedRoute, (newRoute) => {
  drawSelectedRoute(newRoute);
});

// Observar cuando se cargan todas las rutas
watch(() => props.allRoutes, () => {
  drawAllMarkers();
}, { deep: true });

onMounted(() => {
  initMap();
  drawAllMarkers();
});
</script>

<style>
.leaflet-routing-container { display: none !important; }
</style>