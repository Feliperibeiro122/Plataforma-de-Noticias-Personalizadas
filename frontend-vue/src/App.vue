<script setup>
import { ref } from 'vue'
import axios from 'axios'

import { onMounted } from 'vue'; // Verifique se já importou o onMounted

const verificandoAuth = ref(true); 

onMounted(async () => {
  const token = localStorage.getItem('token');
  if (token) {
    await carregarFeed(); // Espera carregar os dados ANTES de liberar a tela
  }
  verificandoAuth.value = false; // Só agora paramos de verificar
});

const logout = () => {
  localStorage.removeItem('token'); // Remove a "chave" de acesso
  isLoggedIn.value = false;         // Volta para a tela de login
  noticias.value = [];              // Limpa os dados por segurança
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

    // 1. Busca as noticias
    const resFeed = await axios.get(`${API_URL}/feed`, {
      headers: {Authorization: `Bearer ${token}`}
    });

    //2. Busca os seus favoritos salvos no banco
    const resFavs = await axios.get(`${API_URL}/favorites`, {
      headers: {Authorization: `Bearer ${token}`}
    });

    const listaNoticias = resFeed.data.noticias || resFeed.data;
    const meusFavoritos = resFavs.data;

    //Acesso a chave "Noticias" definida no main.py e se o link da notícia estiver nos favoritos, marca como true
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

    //Inverte o estado visual primeiro para ser instantâneo para o usuário
    noticia.favorito = !noticia.favorito;

    if (noticia.favorito) {
      //Se agora é favorito, salva no banco
      await axios.post(`${API_URL}/favorites`, {
        title: noticia.title,
        url: noticia.url,
        image_url: noticia.urlToImage
      }, {
        headers: { Authorization: `Bearer ${token}`}
      });
      console.log("Favorito salvo no banco");
    } else {
      //Tarefa para depois: Criar a rota de DELETE no backend para remover
      console.log("Removido (lógica de delete ainda não integrada)");
    }
  } catch (error) {
    console.error("Erro ao salvar favorito:", error);
    //Caso dê errom volta o estado da estrela para o anterior
    noticia.favorito = !noticia.favorito;
    alert("Não foi possível salvar o favorito");
  }
}
</script>

<template>
  <div class="login-container">
    
    <div v-if="verificandoAuth" class="loading-screen">
      <h1 class="neon-text">CARREGANDO...</h1>
    </div>

    <div v-else-if="!isLoggedIn" id="auth-form">
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

    <div v-else class="main-feed">
      <header class="feed-header">
        <h1 class="neon-text">SEU FEED</h1>
        <button @click="logout" class="logout-btn">Sair</button>
      </header>

      <div class="feed-container">
        <div v-for="item in noticias" :key="item.url" class="news-card">
          <h3 class="neon-text-small">{{ item.title }}</h3>
          <p>{{ item.description }}</p>

          <div class="card-actions">
            <a :href="item.url" target="_blank" class="read-more">Ler notícia</a>
            <button @click="toggleFavorito(item)" class="fav-btn">
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

  .feed-header {
    display: grid; /* Mudamos de flex para grid para controle total */
    grid-template-columns: 1fr auto 1fr; /* 3 colunas: as das pontas ocupam o mesmo espaço */
    align-items: center;
    width: 100%;
    max-width: 1200px;
    margin: 20px auto;
    padding: 0 15px;
  }

  /* O título agora fica na coluna do meio (centralizado) */
  .feed-header h1 {
    grid-column: 2; 
    margin: 0; /* Remove margens que podem desalinhá-lo */
  }

  /* O botão de sair fica na terceira coluna (alinhado à direita) */
  .logout-btn {
    grid-column: 3;
    justify-self: end; /* Alinha o botão no fim da sua coluna (direita) */
    width: auto;
    background: #ff4d4d;
    color: white;
    border: 2px solid #ff4d4d;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(255, 77, 77, 0.3);
  }

  .logout-btn:hover {
    background: transparent;
    color: #ff4d4d;
    box-shadow: 0 0 20px rgba(255, 77, 77, 0.6);
    transform: scale(1.05);
  }

  /* Quando a tela for até que 600px (celulares) */
  @media (max-width: 870px) {
  .feed-header {
    display: flex;        /* Volta para flex em telas pequenas */
    flex-direction: column; /* Coloca um em cima do outro */
    gap: 15px;            /* Espaço entre o título e o botão */
    padding: 10px;
  }

  .feed-header h1 {
    font-size: 1.2rem;    /* Diminui um pouco o título para caber */
    text-align: center;
  }

  .logout-btn {
    width: auto;    
    align-self: center; 
    margin-top: 5px;
  }
}

/* TABLETS (Telas entre 601px e 1024px) */
/* TABLET (Telas de 601px até 1024px) */
@media (min-width: 601px) and (max-width: 1024px) {
  .feed-header {
    display: flex;
    justify-content: space-between; /* No tablet, o 'between' funciona melhor para evitar sobreposição */
    align-items: center;
    padding: 0 30px;
    position: static; /* Remove o absolute do botão nesse tamanho */
  }

  .feed-header h1 {
    flex: 1;
    text-align: left; /* Alinha o texto à esquerda para dar espaço ao botão no canto */
    font-size: 1.3rem;
    margin-right: 20px; /* Margem de segurança para o botão */
  }

  .logout-btn {
    position: static; /* O botão volta a ocupar o seu próprio espaço */
    transform: none;
    flex-shrink: 0;   /* Não deixa o botão encolher */
  }
  
  .feed-container {
    grid-template-columns: repeat(2, 1fr); /* 2 colunas de notícias no tablet */
  }
}
</style>