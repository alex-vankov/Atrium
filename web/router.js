import { createRouter, createWebHistory } from 'vue-router';
import Home from './pages/Home.vue';
import Login from "./pages/Login.vue";
import Profile from "./pages/Profile.vue";
import Register from "./pages/Register.vue";

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/profile', component: Profile },
  { path: '/register', component: Register },
]

const router = createRouter({
  history: createWebHistory(), // Uses HTML5 history mode
  routes,
});

export default router;
