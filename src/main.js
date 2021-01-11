import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App.vue'
import TheMap from './TheMap.vue'


Vue.use(VueRouter);

const routes = [
  {path: '/',
   component: TheMap}
];

const router = new VueRouter({
  routes,
  mode: 'history'
});

new Vue({
  el: '#app',
  render: h => h(App),
  router
})
