<template>
  <div style="margin: 20px; text-align: center;">
    <h2>Trainer Dashboard</h2>
    <p>Hoş geldiniz, Antrenör!</p>
    
    <!-- Navigasyon Linkleri -->
    <div style="margin: 20px;">
      <router-link to="/trainer/programs">
        <button style="margin-right: 10px;">Workout Programları</button>
      </router-link>
      <!-- Diğer antrenör işlemleri için ek linkler ekleyebilirsiniz -->
      <router-link to="/member-dashboard">
        <button style="margin-right: 10px;">Üye Paneli</button>
      </router-link>
      <router-link to="/">
        <button @click="logout">Çıkış Yap</button>
      </router-link>
    </div>
    
    <!-- Panel içeriğini burada gösterebilirsiniz -->
    <div>
      <p>Antrenör olarak özet bilgilerinizi buraya ekleyebilirsiniz.</p>
    </div>
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

<style scoped>
/* İsteğe bağlı stil düzenlemeleri */
button {
  padding: 10px 20px;
  font-size: 16px;
}
</style>
