<template>
    <div style="margin: 20px;">
      <h2>Ödeme Yönetimi</h2>
  
      <!-- Yeni Ödeme Ekleme Formu -->
      <div style="margin-bottom: 30px;">
        <h3>Yeni Ödeme Ekle</h3>
        <form @submit.prevent="addPayment">
          <!-- Kullanıcı Dropdown -->
          <div style="margin-bottom: 10px;">
            <label>Kullanıcı Seçin: </label>
            <select v-model="newPayment.user_id" required>
              <option disabled value="">Kullanıcı Seçin</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.first_name }} {{ user.last_name }} ({{ user.email }})
              </option>
            </select>
          </div>
          <div style="margin-bottom: 10px;">
            <input type="number" v-model="newPayment.product_id" placeholder="Product ID" required />
          </div>
          <div style="margin-bottom: 10px;">
            <input type="number" v-model="newPayment.amount" placeholder="Tutar" required step="0.01" />
          </div>
          <!-- Tarih girişi kaldırıldı, Oracle DEFAULT SYSDATE kullanılacak -->
          <div style="margin-bottom: 10px;">
            <input type="text" v-model="newPayment.status" placeholder="Durum (paid, pending, failed)" required />
          </div>
          <button type="submit">Ödeme Ekle</button>
        </form>
      </div>
  
      <!-- Ödeme Listesi -->
      <div>
        <h3>Ödeme Listesi</h3>
        <table border="1" cellpadding="5" cellspacing="0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Kullanıcı ID</th>
              <th>Product ID</th>
              <th>Tutar</th>
              <th>Ödeme Tarihi</th>
              <th>Durum</th>
              <th>İşlemler</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payment in payments" :key="payment.id">
              <td>{{ payment.id }}</td>
              <td>{{ payment.user_id }}</td>
              <td>{{ payment.product_id }}</td>
              <td>{{ payment.amount }}</td>
              <td>{{ payment.payment_date }}</td>
              <td>{{ payment.status }}</td>
              <td>
                <button @click="prepareUpdate(payment)">Güncelle</button>
                <button @click="deletePayment(payment.id)">Sil</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Ödeme Güncelleme Formu -->
      <div v-if="updatePaymentData" style="margin-top: 30px; border: 1px solid #ccc; padding: 10px;">
        <h3>Ödemeyi Güncelle</h3>
        <form @submit.prevent="updatePayment">
          <div style="margin-bottom: 10px;">
            <label>Tutar: </label>
            <input type="number" v-model="updatePaymentData.amount" required step="0.01" />
          </div>
          <div style="margin-bottom: 10px;">
            <label>Durum: </label>
            <input type="text" v-model="updatePaymentData.status" required />
          </div>
          <!-- Tarih alanı güncelleme formundan kaldırıldı, istenirse eklenebilir -->
          <button type="submit">Güncelle</button>
          <button type="button" @click="cancelUpdate">İptal</button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  const token = localStorage.getItem("token");
  
  const payments = ref([]);
  const users = ref([]);
  const newPayment = ref({
    user_id: "",
    product_id: "",
    amount: 0,
    status: ""
  });
  
  // Güncelleme için kullanılacak değişken
  const updatePaymentData = ref(null);
  
  // Ödemeleri GET isteği ile çek
  const fetchPayments = async () => {
    try {
      const response = await fetch("http://localhost:9000/payments", {
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
      console.error("Fetch error:", error);
    }
  };
  
  // Kullanıcı listesini GET isteği ile çek
  const fetchUsers = async () => {
    try {
      const response = await fetch("http://localhost:9000/users", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        users.value = data.users;
      } else {
        console.error("Kullanıcılar alınamadı, status:", response.status);
      }
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };
  
  // Yeni ödeme ekleme (POST)
  const addPayment = async () => {
    try {
      const response = await fetch("http://localhost:9000/payments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(newPayment.value)
      });
      if (response.ok) {
        alert("Ödeme eklendi!");
        newPayment.value = { user_id: "", product_id: "", amount: 0, status: "" };
        fetchPayments();
      } else {
        const errorData = await response.json();
        alert("Ödeme eklenemedi: " + errorData.detail);
      }
    } catch (error) {
      console.error("Ödeme ekleme hatası:", error);
    }
  };
  
  // Ödeme silme (DELETE)
  const deletePayment = async (id) => {
    try {
      const response = await fetch(`http://localhost:9000/payments/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (response.ok) {
        alert("Ödeme silindi!");
        fetchPayments();
      } else {
        alert("Ödeme silinemedi!");
      }
    } catch (error) {
      console.error("Ödeme silme hatası:", error);
    }
  };
  
  // Güncelleme formunu açmak için ödeme verilerini kopyalıyoruz
  const prepareUpdate = (payment) => {
    updatePaymentData.value = { ...payment };
  };
  
  // Güncelleme işlemini iptal etmek için
  const cancelUpdate = () => {
    updatePaymentData.value = null;
  };
  
  // Ödeme güncelleme (PUT)
  const updatePayment = async () => {
    try {
      const response = await fetch(`http://localhost:9000/payments/${updatePaymentData.value.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(updatePaymentData.value)
      });
      if (response.ok) {
        alert("Ödeme güncellendi!");
        updatePaymentData.value = null;
        fetchPayments();
      } else {
        const errorData = await response.json();
        alert("Ödeme güncellenemedi: " + errorData.detail);
      }
    } catch (error) {
      console.error("Ödeme güncelleme hatası:", error);
    }
  };
  
  onMounted(() => {
    fetchPayments();
    fetchUsers();
  });
  </script>
  