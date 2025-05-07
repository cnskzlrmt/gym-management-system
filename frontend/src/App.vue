<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ChatWidget from './components/ChatWidget.vue'

// Geçerli route bilgisini alıyoruz
const route = useRoute()

// Sadece token varsa ve route login veya register değilse ChatWidget'ı göster
const showChatWidget = computed(() => {
  const token = localStorage.getItem('token')
  const hideOnPaths = ['/', '/register']  // Login ve register sayfalarında gizle
  return token && !hideOnPaths.includes(route.path)
})
</script>

<template>
  <div id="app">
    <router-view />
    <!-- Yalnızca yetkilendirme yapılmış ve login/register sayfası dışında ise göster -->
    <ChatWidget v-if="showChatWidget" />
  </div>
</template>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}
</style>
