<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const userInput = ref('')
const messages = ref([])

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const sendMessage = async () => {
  const question = userInput.value.trim()
  if (!question) return

  // Kullanıcının mesajını listeye ekle
  messages.value.push({ sender: 'user', text: question })
  userInput.value = ''

  try {
    // localStorage'dan token'ı alıyoruz
    const token = localStorage.getItem('token')
    
    const response = await axios.post(
      'http://localhost:9000/chatbot',
      { question },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    
    if (response.data && response.data.results) {
      messages.value.push({ sender: 'bot', text: JSON.stringify(response.data.results) })
    } else {
      messages.value.push({ sender: 'bot', text: 'Üzgünüm, bir sorun oluştu.' })
    }
  } catch (error) {
    messages.value.push({ sender: 'bot', text: 'Hata: ' + error.message })
  }
}
</script>

<template>
  <div class="chat-widget">
    <button v-if="!isOpen" class="chat-toggle-button" @click="toggleChat">Chat</button>
    
    <div v-if="isOpen" class="chat-window">
      <div class="chat-header">
        <span>Chatbot</span>
        <button class="close-button" @click="toggleChat">X</button>
      </div>
      <div class="chat-body">
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="message"
          :class="message.sender"
        >
          {{ message.text }}
        </div>
      </div>
      <div class="chat-footer">
        <input
          type="text"
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="Soru yazın..."
        />
        <button @click="sendMessage">Gönder</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}
.chat-toggle-button {
  background-color: #007bff;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
.chat-window {
  width: 300px;
  height: 400px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}
.chat-header {
  background-color: #007bff;
  color: #fff;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close-button {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}
.chat-body {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}
.message {
  margin-bottom: 8px;
  word-wrap: break-word;
}
.message.user {
  text-align: right;
  color: #007bff;
}
.message.bot {
  text-align: left;
  color: #333;
}
.chat-footer {
  padding: 10px;
  display: flex;
}
.chat-footer input[type="text"] {
  flex: 1;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.chat-footer button {
  margin-left: 5px;
  padding: 5px 10px;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}
</style>
