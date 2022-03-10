import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  }, {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }, {
    path: '/static-vis',
    name: 'Static-Vis',
    component: () => import('../views/Static.vue')
  }, {
    path: '/template',
    name: 'Template',
    component: () => import('../views/Template.vue')
  }, {
    path: '/dynamic-vis',
    name: 'Dynamic-Vis',
    component: () => import ('../views/Dynamic.vue')
  }, {
    path: '/wine',
    name: 'Wine',
    component: () => import ('../views/Wine.vue')
  },{
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