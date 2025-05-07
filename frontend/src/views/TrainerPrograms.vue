<template>
    <div style="margin: 20px;">
      <h2>Trainer Paneli - Workout Programları</h2>
      
      <!-- Yeni Program Ekleme Formu -->
      <div style="margin-bottom: 30px; border: 1px solid #ccc; padding: 10px;">
        <h3>Yeni Workout Programı Ekle</h3>
        <form @submit.prevent="addProgram">
          <!-- Üye Seçimi Dropdown -->
          <div style="margin-bottom: 10px;">
            <label>Üye Seçin: </label>
            <select v-model="newProgram.user_id" required>
              <option disabled value="">Üye Seçin</option>
              <option v-for="member in members" :key="member.id" :value="member.id">
                {{ member.first_name }} {{ member.last_name }} ({{ member.email }})
              </option>
            </select>
          </div>
          <div style="margin-bottom: 10px;">
            <input type="text" v-model="newProgram.name" placeholder="Program Adı" required />
          </div>
          <div style="margin-bottom: 10px;">
            <textarea v-model="newProgram.description" placeholder="Program Açıklaması" rows="3"></textarea>
          </div>
          <button type="submit">Program Ekle</button>
        </form>
      </div>
      
      <!-- Workout Programları Listesi -->
      <div>
        <h3>Workout Programlarım</h3>
        <table border="1" cellpadding="5" cellspacing="0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Üye ID</th>
              <th>Program Adı</th>
              <th>Açıklama</th>
              <th>Oluşturulma Tarihi</th>
              <th>İşlemler</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="program in programs" :key="program.id">
              <td>{{ program.id }}</td>
              <td>{{ program.user_id }}</td>
              <td>{{ program.name }}</td>
              <td>{{ program.description }}</td>
              <td>{{ program.created_at }}</td>
              <td>
                <button @click="deleteProgram(program.id)">Sil</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const token = localStorage.getItem("token");
  
  // Trainer'ın workout programlarını saklamak için
  const programs = ref([]);
  // Üye listesini dropdown için saklamak
  const members = ref([]);
  // Yeni program formundaki veriler
  const newProgram = ref({
    user_id: "",
    name: "",
    description: ""
  });
  
  // Antrenörün kendi workout programlarını çekmek için GET isteği
  const fetchPrograms = async () => {
    try {
      const response = await fetch("http://localhost:9000/workout-programs", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        programs.value = data.workout_programs;
      } else {
        console.error("Programlar alınamadı, status:", response.status);
      }
    } catch (error) {
      console.error("Program fetch error:", error);
    }
  };
  
  // Üye listesini çekmek için GET isteği (Admin tarafından sağlanıyor)
  const fetchMembers = async () => {
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
        members.value = data.users;
      } else {
        console.error("Üyeler alınamadı, status:", response.status);
      }
    } catch (error) {
      console.error("Members fetch error:", error);
    }
  };
  
  // Yeni program ekleme (POST isteği)
  const addProgram = async () => {
    try {
      const response = await fetch("http://localhost:9000/workout-programs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          user_id: newProgram.value.user_id,   // Seçilen üyenin ID'si
          name: newProgram.value.name,
          description: newProgram.value.description,
          created_at: new Date().toISOString()  // Backend CURRENT_TIMESTAMP da kullanabilir
        })
      });
      if (response.ok) {
        alert("Program eklendi!");
        newProgram.value = { user_id: "", name: "", description: "" };
        fetchPrograms();
      } else {
        const errorData = await response.json();
        alert("Program eklenemedi: " + errorData.detail);
      }
    } catch (error) {
      console.error("Program ekleme hatası:", error);
    }
  };
  
  // Program silme (DELETE isteği)
  const deleteProgram = async (id) => {
    try {
      const response = await fetch(`http://localhost:9000/workout-programs/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (response.ok) {
        alert("Program silindi!");
        fetchPrograms();
      } else {
        alert("Program silinemedi!");
      }
    } catch (error) {
      console.error("Program silme hatası:", error);
    }
  };
  
  onMounted(() => {
    fetchPrograms();
    fetchMembers();
  });
  </script>
  