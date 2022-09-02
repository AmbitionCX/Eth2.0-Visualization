import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/epoch',
    name:'Epoch',
    component: () => import('../components/Epoch.vue')
  },{
    path: '/overview',
    name:'Overview',
    component: () => import('../components/Overview.vue')
  },{
    path: '/slot',
    name:'Slot',
    component: () => import('../components/Slot.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router