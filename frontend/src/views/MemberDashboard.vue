<template>
  <div style="margin: 20px;">
    <h2>Üyelik Paneli</h2>
    
    
    <!-- Profil Bilgileri -->
    <section style="margin-top: 20px;">
      <h3>Profil Bilgileri</h3>
      <div v-if="profile">
        <p><strong>Ad Soyad:</strong> {{ profile.first_name }} {{ profile.last_name }}</p>
        <p><strong>Email:</strong> {{ profile.email }}</p>
        <p><strong>Telefon:</strong> {{ profile.phone || "Belirtilmemiş" }}</p>
        <p><strong>Üyelik Durumu:</strong> {{ profile.is_active ? "Aktif" : "Pasif" }}</p>
      </div>
      <div v-else>
        <p>Profil bilgileri yükleniyor...</p>
      </div>
    </section>
    
    <!-- Ödeme Geçmişi -->
    <section style="margin-top: 30px;">
      <h3>Ödeme Geçmişi</h3>
      <div v-if="payments.length > 0">
        <table border="1" cellpadding="5" cellspacing="0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Tutar</th>
              <th>Tarih</th>
              <th>Durum</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payment in payments" :key="payment.id">
              <td>{{ payment.id }}</td>
              <td>{{ payment.amount }}</td>
              <td>{{ payment.payment_date }}</td>
              <td>{{ payment.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Ödeme geçmişi bulunamadı.</p>
      </div>
    </section>
    
    <!-- Workout Programları -->
    <section style="margin-top: 30px;">
      <h3>Workout Programları</h3>
      <div v-if="workoutPrograms.length > 0">
        <table border="1" cellpadding="5" cellspacing="0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Trainer ID</th>
              <th>Program Adı</th>
              <th>Açıklama</th>
              <th>Oluşturulma Tarihi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="program in workoutPrograms" :key="program.id">
              <td>{{ program.id }}</td>
              <td>{{ program.trainer_id }}</td>
              <td>{{ program.name }}</td>
              <td>{{ program.description }}</td>
              <td>{{ program.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Workout programı bulunamadı.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const token = localStorage.getItem("token");

const profile = ref(null);
const payments = ref([]);
const workoutPrograms = ref([]);

// Üye profilini API üzerinden çekiyoruz
const fetchProfile = async () => {
  try {
    const response = await fetch("http://localhost:9000/member/profile", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });
    if (response.ok) {
      profile.value = await response.json();
    } else {
      console.error("Profil bilgileri alınamadı, status:", response.status);
    }
  } catch (error) {
    console.error("Profile fetch error:", error);
  }
};

// Ödeme geçmişini API üzerinden çekiyoruz
const fetchPayments = async () => {
  try {
    const response = await fetch("http://localhost:9000/member/payments", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      payments.value = data.payments;
    } else {
      console.error("Ödeme bilgileri alınamadı, status:", response.status);
    }
  } catch (error) {
    console.error("Payments fetch error:", error);
  }
};

// Workout programlarını API üzerinden çekiyoruz
const fetchWorkoutPrograms = async () => {
  try {
    const response = await fetch("http://localhost:9000/member/workout-program", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      workoutPrograms.value = data.workout_programs;
    } else {
      console.error("Workout programları alınamadı, status:", response.status);
    }
  } catch (error) {
    console.error("Workout fetch error:", error);
  }
};

onMounted(() => {
  fetchProfile();
  fetchPayments();
  fetchWorkoutPrograms();
});
</script>
