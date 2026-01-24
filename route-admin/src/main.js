import { createApp } from 'vue'

// --- 1. IMPORTA LOS PLUGINS QUE NECESITAS ---
import { Quasar, Screen, Notify } from 'quasar' 

// Importa los extras de Quasar y el CSS
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'

import App from './App.vue'
import router from './router';

const myApp = createApp(App)

myApp.use(Quasar, {
  // --- 2. AÑADE LOS PLUGINS AQUÍ ---
  plugins: {
    Screen, // Plugin para detectar el tamaño de la pantalla (soluciona tu error)
    Notify  // Plugin muy útil para mostrar notificaciones en el futuro
  }, 
})

myApp.use(router);

myApp.mount('#app')
