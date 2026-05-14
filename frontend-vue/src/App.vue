<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import TheHeader from './components/TheHeader.vue'
import SkeletonCard from './components/SkeletonCard.vue'
import NewsCard from './components/NewsCard.vue'

const verificandoAuth = ref(true); 

onMounted(async () => {
  const token = localStorage.getItem('token');
  if (token) {
    await carregarFeed(); 
  }
  verificandoAuth.value = false; 
});

const logout = () => {
  localStorage.removeItem('token'); 
  isLoggedIn.value = false;         
  noticias.value = [];              
};

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
      await carregarFeed() 
      isLoggedIn.value = true 
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
    
    // 1. Busca as noticias
    const resFeed = await axios.get(`${API_URL}/feed`, {
      headers: {Authorization: `Bearer ${token}`}
    });

    // 2. Busca os seus favoritos salvos no banco
    const resFavs = await axios.get(`${API_URL}/favorites`, {
      headers: {Authorization: `Bearer ${token}`}
    });

    const listaNoticias = resFeed.data.noticias || resFeed.data;
    const meusFavoritos = resFavs.data;

    noticias.value = listaNoticias.map(noticia => {
      const jaFavoritado = meusFavoritos.some(fav => fav.url === noticia.url);
      return { ...noticia, favorito: jaFavoritado};
    });
    isLoggedIn.value = true
  } catch(error) {
    console.error("Erro ao carregar feed e favoritos:",error)
  }
}

const toggleFavorito = async (noticia) => {
  try {
    const token = localStorage.getItem('token');
    noticia.favorito = !noticia.favorito;

    if (noticia.favorito) {
      await axios.post(`${API_URL}/favorites`, {
        title: noticia.title,
        url: noticia.url,
        image_url: noticia.urlToImage
      }, {
        headers: { Authorization: `Bearer ${token}`}
      });
      console.log("Favorito salvo no banco");
    } else {
      console.log("Removido (lógica de delete ainda não integrada)");
    }
  } catch (error) {
    console.error("Erro ao salvar favorito:", error);
    noticia.favorito = !noticia.favorito;
    alert("Não foi possível salvar o favorito");
  }
}
</script>

<template>
  <div class="login-container">
    
   <div v-if="!isLoggedIn && !verificandoAuth" id="auth-form">
      <h1 class="neon-text">PLATAFORMA DE NOTÍCIAS</h1>
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

    <div v-else-if="isLoggedIn || verificandoAuth" class="main-feed">
      <TheHeader :verificandoAuth="verificandoAuth" @logout="logout" />

      <div class="feed-container">
        <template v-if="verificandoAuth">
          <SkeletonCard v-for="n in 6" :key="n" />
        </template>

        <template v-else>
          <NewsCard 
            v-for="item in noticias" 
            :key="item.url" 
            :item="item"
            @toggle-fav="toggleFavorito"
          />
        </template>
      </div>
    </div>

  </div>
</template>

<style>
  :root {
    --primary: #6366f1; 
    --bg: #0f172a;      
    --card: #1e293b;    
    --text: #f8fafc;
  }

  body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      margin: 0;
      min-height: 100vh; 
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
      max-width: 800px;
  }

  .main-feed {
      width: 100%;
      max-width: 1200px; 
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px;
  }

  .feed-container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      width: 100%;
      margin-top: 20px;
  }

  .news-card {
      background: var(--card);
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 20px;
      box-sizing: border-box; 
      display: flex;
      flex-direction: column;
      justify-content: space-between; 
      transition: transform 0.3s, border-color 0.3s;
  }

  .news-card:hover {
      transform: translateY(-4px);
      border-color: var(--primary);
  }

  h1.neon-text {
      font-size: 1.5rem;
      margin-bottom: 1.5rem;
      text-align: center;
      color: var(--primary);
      letter-spacing: 1px;
  }

  #form-title {
      text-align: center;
      margin-bottom: 20px;
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

  @media (min-width: 601px) and (max-width: 1024px) {
    .feed-container {
      grid-template-columns: repeat(2, 1fr); 
    }
  }

  @media (min-width: 1025px) {
    .news-card:has(.skeleton) {
      min-height: 250px; 
    }
    
    .feed-container {
      grid-template-columns: repeat(3, 1fr) !important; 
    }
    
    .news-card {
      min-height: 280px;
      display: flex;
      flex-direction: column;
    }
  }
</style>