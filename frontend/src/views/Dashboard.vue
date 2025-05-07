<template>
  <div style="text-align: center; margin-top: 50px;">
    <h2>Admin Dashboard</h2>
    <p>Hoş geldiniz, Admin!</p>
    <router-link to="/dashboard/products">
      <button>Ürün Yönetimi</button>
    </router-link>
    <router-link to="/dashboard/payments" style="margin-left: 20px;">
      <button>Ödeme Yönetimi</button>
    </router-link>
    <router-link to="/trainer/programs">
  <button>Trainer Paneli</button>
</router-link>

    <button @click="logout" style="margin-left: 20px;">Çıkış Yap</button>
    
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/");
};
</script>
