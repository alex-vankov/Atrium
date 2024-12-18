import { createRouter, createWebHistory } from 'vue-router';
import Home from './pages/Home.vue';

const routes = [
  { path: '/', component: Home }
]

const router = createRouter({
  history: createWebHistory(), // Uses HTML5 history mode
  routes,
});

export default router;
