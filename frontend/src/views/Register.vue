<template>
    <div style="text-align: center; margin-top: 50px;">
      <h2>Kayıt Ol</h2>
      <form @submit.prevent="registerUser">
        <input
          type="text"
          v-model="first_name"
          placeholder="Ad"
          required
          style="padding: 8px; width: 250px; margin-bottom: 10px;"
        />
        <br />
        <input
          type="text"
          v-model="last_name"
          placeholder="Soyad"
          required
          style="padding: 8px; width: 250px; margin-bottom: 10px;"
        />
        <br />
        <input
          type="email"
          v-model="email"
          placeholder="Email"
          required
          style="padding: 8px; width: 250px; margin-bottom: 10px;"
        />
        <br />
        <input
          type="password"
          v-model="password"
          placeholder="Şifre"
          required
          style="padding: 8px; width: 250px; margin-bottom: 10px;"
        />
        <br />
        <input
          type="tel"
          v-model="phone"
          placeholder="Telefon"
          required
          style="padding: 8px; width: 250px; margin-bottom: 10px;"
        />
        <br />
        <select
          v-model="role"
          required
          style="padding: 8px; width: 250px; margin-bottom: 10px;"
        >
          <option value="member">Üye</option>
          <option value="trainer">Antrenör</option>
          <option value="admin">Admin</option>
        </select>
        <br />
        <button type="submit" style="padding: 10px 20px;">Kayıt Ol</button>
      </form>
      <p v-if="message" :style="{ color: messageType === 'error' ? 'red' : 'green', marginTop: '10px' }">
        {{ message }}
      </p>
      <p v-if="loading">İşlem yapılıyor...</p>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  const first_name = ref("");
  const last_name = ref("");
  const email = ref("");
  const password = ref("");
  const phone = ref("");
  const role = ref("member");
  const message = ref("");
  const messageType = ref(""); // 'error' veya 'success'
  const loading = ref(false);
  
  const router = useRouter();
  
  const registerUser = async () => {
    message.value = "";
    loading.value = true;
    const formData = {
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      password: password.value,
      phone: phone.value,
      role: role.value,
    };
  
    try {
      const response = await fetch("http://localhost:9000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Kayıt sırasında hata oluştu.");
      }
      messageType.value = "success";
      message.value = data.message || "Kayıt başarılı!";
      // İsteğe bağlı olarak, kayıt sonrası giriş sayfasına yönlendirme yapabilirsiniz.
      // router.push("/"); veya router.push("/login");
    } catch (error) {
      messageType.value = "error";
      message.value = error.message;
      console.error("Kayıt hatası:", error);
    } finally {
      loading.value = false;
    }
  };
  </script>
  
  <style scoped>
  /* İhtiyacınıza göre stil ekleyebilirsiniz */
  </style>
  