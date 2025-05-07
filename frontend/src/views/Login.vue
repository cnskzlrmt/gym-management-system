<template>
  <div style="text-align: center; margin-top: 50px;">
    <h2>Giriş Sayfası</h2>
    <form @submit.prevent="login">
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
      <button type="submit" style="padding: 10px 20px;">Giriş Yap</button>
      <p v-if="errorMessage" style="color: red; margin-top: 10px;">{{ errorMessage }}</p>
    </form>
    <!-- Kayıt linki ekleniyor -->
    <p style="margin-top: 20px;">
      Hesabınız yok mu? 
      <router-link to="/register">Kayıt Ol</router-link>
    </p>
  </div>
</template>

  
  <script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  const email = ref("");
  const password = ref("");
  const errorMessage = ref("");
  const router = useRouter();
  
  const login = async () => {
    errorMessage.value = "";
  
    try {
      const response = await fetch("http://localhost:9000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username: email.value, password: password.value })
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        throw new Error(data.detail || "Giriş başarısız");
      }
  
      // Gelen JWT token'ı kaydet
      localStorage.setItem("token", data.access_token);
  
      // JWT token'ı decode edip rol bilgisini alalım (payload, tokenın ortasında base64 kodlu)
      const payload = JSON.parse(atob(data.access_token.split(".")[1]));
      localStorage.setItem("role", payload.role);
  
      // Kullanıcının rolüne göre yönlendir
      if (payload.role === "admin") {
        router.push("/dashboard");
      } else if (payload.role === "trainer") {
        router.push("/trainer-dashboard");
      } else if (payload.role === "member") {
        router.push("/member-dashboard");
      } else {
        router.push("/");
      }
    } catch (error) {
      errorMessage.value = error.message;
    }
  };
  </script>
  