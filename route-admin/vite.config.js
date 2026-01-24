// En vite.config.js

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

// --- 1. IMPORTA EL MÓDULO 'path' DE NODE ---
//    'path' es una herramienta interna de Node.js para trabajar con rutas de archivos.
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),
    quasar({
      // --- 2. CAMBIA LA RUTA A UNA RUTA ABSOLUTA ---
      //    __dirname es una variable que contiene la ruta a la carpeta actual (la raíz de tu proyecto).
      //    'resolve' une esa ruta con 'src/quasar-variables.sass' para crear una ruta completa.
      sassVariables: resolve(__dirname, 'src/quasar-variables.sass')
    })
  ]
})