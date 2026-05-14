<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isLogin = ref(true)
const email = ref('')
const password = ref('')
const preferences = ref('')
const API_URL = "http://127.0.0.1:8000"

const isLoggedIn = ref(false)
const noticias = ref([])

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
      alert("Login realizado com sucesso!")
      await carregarFeed() //chama a função que busca as noticias
      isLoggedIn.value = true //Troca a tela de login para o feed
    } else {
      alert("Cadastro ok! Faça Login.")
      isLogin.value = true
    }
  } catch (err) {
    alert(err.response?.data?.detail || "Erro na conexão")
  }
}

const carregarFeed = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/feed`, {
      headers: { Authorization: `Bearer ${token}`}
    })

    //Acesso a chave "Noticias" definida no main.py 
    noticias.value = response.data.noticias
    isLoggedIn.value = true
  } catch(error) {
    console.error("Erro ao carregar feed:",error)
  }
}
</script>

<template>
  <div class="login-container">
    <div v-if="!isLoggedIn" id="auth-form">
      <h1 class="neon-text">PLATAFORMA DE NOTÍCIAS PERSONALIZADAS</h1>
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

    <div v-else class="main-feed">
      <h1 class="neon-text">SEU FEED</h1>

      <div class="feed-container">
        <div v-for="item in noticias" :key="item.url" class="news-card">
        <h3 class="neon-text-small">{{ item.title }}</h3>
        <p>{{ item.description }}</p>

        <div class="card-actions">
          <a :href="item.url" target="_blank" class="read-more">Ler notícia</a>

          <button @click="item.favorito = !item.favorito" class="fav-btn">
            {{ item.favorito ? '⭐' : '☆' }}
          </button>
        </div>
      </div>
      </div>
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
      margin: 0;
      min-height: 100vh; /* Usa no mínimo a altura da tela, mas cresce se precisar */
      display: flex;
      flex-direction: column;
      align-items: center;
  }

  .login-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
      width: 100%;
      max-width: 800px; /* Evita que o feed fique largo demais */
  }

  .main-feed {
      width: 100%;
      max-width: 1200px; /* Largura máxima confortável */
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px;
  }

  .feed-container {
      display: grid;
      /* auto-fit: preenche o espaço / minmax: não deixa o card ficar menor que 280px */
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      width: 100%;
      margin-top: 20px;
  }

  /* Isso garante que o card não "estoure" o layout */
  .news-card {
      background: var(--card);
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 20px;
      box-sizing: border-box; /* Importante para a responsividade */
      display: flex;
      flex-direction: column;
      justify-content: space-between; /* Empurra o botão de ler mais para o fim do card */
  }

  .news-card:hover {
      transform: translateY(-4px);
      border-color: var(--primary);
  }

  .card-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 15px;
  }

  .read-more {
      color: var(--primary);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 600;
  }

  .fav-btn {
      background: none;
      width: auto; /* Para o botão de estrela não virar um blocão */
      padding: 5px;
      margin: 0;
      font-size: 1.2rem;
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