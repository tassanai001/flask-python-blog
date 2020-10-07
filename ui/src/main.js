// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Buefy from 'buefy'

import App from './App'
import router from './router'

import 'buefy/dist/buefy.css'
import './assets/css/main.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faTrash,
  faCog,
  faArrowLeft,
  faPlus,
  faArrowUp
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import VModal from 'vue-js-modal'

library.add(faTrash, faCog, faArrowLeft, faPlus, faArrowUp)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(Buefy)
Vue.use(require('vue-moment'))
Vue.use(VModal, { dialog: true })

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
