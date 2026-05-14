<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isLogin = ref(true)
const email = ref('')
const password = ref('')
const preferences = ref('')
const API_URL = "http://127.0.0.1:8000"

const toggleMode = () => {
  isLogin.value = !isLogin.value
}

const handleAuth = async () => {
  try {
    const endpoint = isLogin.value ? '/login' : '/register'
    const payload = {email: email.value, password: password.value, preferences: preferences.value}

    const {data} = await axios.post(`${API_URL}${endpoint}`, payload)

    if (isLogin.value) {
      localStorage.setItem('token', data.access_token)
      alert("Sucesso! Partindo para o Feed...")
      // Aqui será feito a troca de página depois
    } else {
      alert("Cadastro ok! Faça Login.")
      isLogin.value = true
    }
  } catch (err) {
    alert(err.response?.data?.detail || "Erro na conexão")
  }
}
</script>

<template>
  <div class="login-container">
    <h1 class="neon-text">PLATAFORMA DE NOTÍCIAS PERSONALIZADAS</h1>

    <div id="auth-form">
      <h2 id="form-title">{{ isLogin ? 'Login' : 'Cadastro' }}</h2>
      
      <input type="email" v-model="email" placeholder="E-mail" required>
      <input type="password" v-model="password" placeholder="Senha" required>
      
      <input 
        v-if="!isLogin" 
        type="text" 
        v-model="preferences" 
        placeholder="Suas preferências (ex: tech, natureza)"
      >

      <button @click="handleAuth" id="auth-btn">
        {{ isLogin ? 'Entrar' : 'Cadastrar' }}
      </button>
      
      <p @click="toggleMode" id="toggle-text">
        {{ isLogin ? 'Não tem conta? Cadastre-se' : 'Já tem conta? Faça Login' }}
      </p>
    </div>
  </div>
</template>

<style>
  :root {

    --primary: #6366f1; /* Um roxo/azul moderno */
    --bg: #0f172a;      /* Azul marinho bem escuro */
    --card: #1e293b;    /* Cinza azulado para o formulário */
    --text: #f8fafc;
  }

  body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
  }

  .login-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
  }

  h1 {
      font-size: 1.5rem;
      margin-bottom: 1.5rem;
      text-align: center;
      color: var(--primary);
      letter-spacing: 1px;
  }

  input {
      width: 100%;
      padding: 12px;
      margin: 8px 0;
      background: #0f172a;
      border: 1px solid #334155;
      color: white;
      border-radius: 6px;
      box-sizing: border-box;
      transition: border 0.3s;
  }

  input:focus {
      border-color: var(--primary);
      outline: none;
  }

  button {
      width: 100%;
      padding: 12px;
      background: var(--primary);
      border: none;
      color: white;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 10px;
      transition: filter 0.3s;
  }

  button:hover {
      filter: brightness(1.2);
  }

  #toggle-text {
      text-align: center;
      font-size: 0.85rem;
      margin-top: 20px;
      cursor: pointer;
      color: #94a3b8;
  }

  #toggle-text:hover {
      color: var(--primary);
  }
</style>