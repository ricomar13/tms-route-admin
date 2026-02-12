import { createApp } from 'vue'
import { Quasar, Notify, Dialog } from 'quasar' 
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import App from './App.vue'
import router from './router'

const myApp = createApp(App)

myApp.use(Quasar, {
  plugins: { Notify, Dialog }, // <-- ACTIVAR AQUÍ
  config: {
    notify: { /* config global opcional */ }
  }
})

myApp.use(router)
myApp.mount('#app')