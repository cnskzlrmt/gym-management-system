import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import TrainerDashboard from "../views/TrainerDashboard.vue";
import MemberDashboard from "../views/MemberDashboard.vue";
import ProductManagement from "../views/ProductManagement.vue";
import PaymentManagement from "../views/PaymentManagement.vue";
import TrainerPrograms from "../views/TrainerPrograms.vue"; // Yeni oluşturduğumuz dosya
import Register from "../views/Register.vue"


const routes = [
  { path: "/", component: Login },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true, role: "admin" } },
  { path: "/register", component: Register },
  { path: "/trainer-dashboard", component: TrainerDashboard, meta: { requiresAuth: true, role: "trainer" } },
  { path: "/member-dashboard", component: MemberDashboard, meta: { requiresAuth: true, role: "member" } },
  { path: "/dashboard/products", component: ProductManagement, meta: { requiresAuth: true, role: "admin" } },
  { path: "/dashboard/payments", component: PaymentManagement, meta: { requiresAuth: true, role: "admin" } },
  { path: "/trainer/programs", component: TrainerPrograms, meta: { requiresAuth: true, role: "trainer" } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  if (to.meta.requiresAuth && !token) {
    next("/");
  } else if (to.meta.role) {
    const storedRole = localStorage.getItem("role");
    if (storedRole !== to.meta.role) {
      return next("/");
    }
    next();
  } else {
    next();
  }
});

export default router;