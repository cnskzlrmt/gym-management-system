<template>
    <div style="margin: 20px;">
      <h2>Ürün Yönetimi</h2>
  
      <!-- Yeni Ürün Ekleme Formu -->
      <div style="margin-bottom: 30px;">
        <h3>Yeni Ürün Ekle</h3>
        <form @submit.prevent="addProduct">
          <div>
            <input type="text" v-model="newProduct.product_type" placeholder="Ürün Tipi (membership/class)" required />
          </div>
          <div>
            <input type="text" v-model="newProduct.name" placeholder="Ürün Adı" required />
          </div>
          <div>
            <input type="number" v-model="newProduct.price" placeholder="Fiyat" required step="0.01" />
          </div>
          <div>
            <input type="number" v-model="newProduct.duration" placeholder="Süre (opsiyonel)" />
          </div>
          <div>
            <input type="text" v-model="newProduct.description" placeholder="Açıklama (opsiyonel)" />
          </div>
          <button type="submit">Ürün Ekle</button>
        </form>
      </div>
  
      <!-- Ürün Listesi -->
      <div>
        <h3>Ürün Listesi</h3>
        <table border="1" cellpadding="5" cellspacing="0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Ürün Tipi</th>
              <th>Ad</th>
              <th>Fiyat</th>
              <th>Süre</th>
              <th>Açıklama</th>
              <th>İşlemler</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>{{ product.id }}</td>
              <td>{{ product.product_type }}</td>
              <td>{{ product.name }}</td>
              <td>{{ product.price }}</td>
              <td>{{ product.duration }}</td>
              <td>{{ product.description }}</td>
              <td>
                <button @click="deleteProduct(product.id)">Sil</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  const token = localStorage.getItem("token"); // Token'ı al
  
  const products = ref([]);
  const newProduct = ref({
    product_type: '',
    name: '',
    price: 0,
    duration: null,
    description: ''
  });
  
  // ✅ Ürünleri GET isteği ile çek (Yetkilendirme Header Eklendi!)
  const fetchProducts = async () => {
    try {
      const response = await fetch("http://localhost:9000/products", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` // 🚀 Token'ı header'a ekledik!
        }
      });
  
      if (response.ok) {
        const data = await response.json();
        products.value = data.products;
      } else {
        console.error("Ürünler alınamadı. Yetkisiz erişim olabilir.");
      }
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };
  
  // ✅ Ürün ekleme POST isteği (Yetkilendirme Header Eklendi!)
  const addProduct = async () => {
    try {
      const response = await fetch("http://localhost:9000/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`  // Yetkilendirme header'ı eklendi
        },
        body: JSON.stringify(newProduct.value)
      });
  
      if (response.ok) {
        alert("Ürün eklendi!");
        newProduct.value = { product_type: '', name: '', price: 0, duration: null, description: '' };
        fetchProducts();
      } else {
        const errorData = await response.json();
        alert("Ürün eklenemedi: " + errorData.detail);
      }
    } catch (error) {
      console.error("Ürün ekleme hatası:", error);
    }
  };
  
  // ✅ Ürün silme DELETE isteği (Yetkilendirme Header Eklendi!)
  const deleteProduct = async (id) => {
    try {
      const response = await fetch(`http://localhost:9000/products/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`  // Yetkilendirme header'ı eklendi
        }
      });
  
      if (response.ok) {
        alert("Ürün silindi!");
        fetchProducts();
      } else {
        alert("Ürün silinemedi!");
      }
    } catch (error) {
      console.error("Ürün silme hatası:", error);
    }
  };
  
  // ✅ Sayfa açıldığında ürünleri çek
  onMounted(() => {
    fetchProducts();
  });
  </script>
  