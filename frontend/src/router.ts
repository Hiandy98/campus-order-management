import { createRouter, createWebHistory } from 'vue-router'
import OrderView from './views/OrderView.vue'
import KitchenView from './views/KitchenView.vue'
import PickupView from './views/PickupView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: OrderView },
    { path: '/kitchen', component: KitchenView },
    { path: '/pickup', component: PickupView },
  ],
})