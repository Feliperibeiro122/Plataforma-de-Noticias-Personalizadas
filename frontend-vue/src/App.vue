<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import TheHeader from './components/TheHeader.vue'
import SkeletonCard from './components/SkeletonCard.vue'
import NewsCard from './components/NewsCard.vue'
import FilterBar from './components/FilterBar.vue'
import TheSidebar from './components/TheSidebar.vue'

const verificandoAuth = ref(true); 

onMounted(async () => {
  window.onscroll = () => {

    if (modoAtual.value !== 'geral') return; 

    if (noticia.value.length === 0)
    return;
    // Detecta se chegou no fim da página (com margem de 100px)
    let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight >= document.documentElement.offsetHeight - 100;

    if (bottomOfWindow && !carregandoMais.value) {
      // Ele continua carregando usando os filtros que já estão salvos
      carregarFeed(filtrosAtuais.value, false); 
    }
  }

  const token = localStorage.getItem('token');
  if (token) {
    isLoggedIn.value = true; // Garante que o estado de login mude
    await carregarFeed({}, true); 
  }
  verificandoAuth.value = false; 
});

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('userId') 
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
const paginaAtual = ref(1)
const carregandoMais = ref(false)
const filtrosAtuais = ref({search: '', category: ''});

const favoritosLista = ref([]);
const historicoLista = ref([]);

const sidebarAberta = ref(false);

const toggleSidebar = () => {
  sidebarAberta.value = !sidebarAberta.value
}


const handleFilterChange = async(novosFiltros) => {
  filtrosAtuais.value = novosFiltros;

  await carregarFeed(novosFiltros, true);
}


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
      const idParaSalvar = data.user_id || data.id || data.user?.id
      if (idParaSalvar) {
        localStorage.setItem('userId', idParaSalvar)
      }
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

const carregarFeed = async (filtros = {}, novaBusca = false) => {
  // 1. Se já estiver carregando, evita chamadas duplicadas
  if (carregandoMais.value) return;

  try {
    carregandoMais.value = true;
    const token = localStorage.getItem('token');

    //2. Se mudou filtro ou tag, página é resetado para a página 1 e esvazia a lista
    if (novaBusca) {
      paginaAtual.value = 1
      noticias.value = [];
    }

    const params = new URLSearchParams();
    params.append('page', paginaAtual.value);
    params.append('size',12)
    
    // Garantir que estamos pegando os nomes certos que o FilterBar envia
    if (filtros.search) params.append('search', filtros.search);
    if (filtros.category) params.append('category', filtros.category);

    if (filtros.dateFrom) params.append('from', filtros.dateFrom);
    if (filtros.dateTo) params.append('to', filtros.dateTo);
    if (filtros.source) params.append('source', filtros.source);

    const queryString = params.toString();
    // A interrogação DEVE estar ali se houver query string
    const urlFinal = queryString ? `${API_URL}/feed?${queryString}` : `${API_URL}/feed`;
    
    const [resFeed, resFavs, resHist] = await Promise.all([
      axios.get(urlFinal, { headers: { Authorization: `Bearer ${token}` } }),
      axios.get(`${API_URL}/favorites`, { headers: { Authorization: `Bearer ${token}` } }),
      axios.get(`${API_URL}/history`, { headers: { Authorization: `Bearer ${token}` } })
    ]);

    // Se o backend retornar um objeto com a chave "noticias", pegamos ela
    const novasNoticiasRaw = resFeed.data.noticias || resFeed.data;
    const meusFavoritos = resFavs.data || [];
    const meuHistorico = resHist.data || [];

    favoritosLista.value = meusFavoritos;
    historicoLista.value = meuHistorico;

    noticias.value = Array.isArray(novasNoticiasRaw) 
      ? novasNoticiasRaw.map(noticia => {
          const jaFavoritado = meusFavoritos.some(fav => fav.url === noticia.url);
          return { 
            ...noticia,
            fonte: noticia.source?.name || 'Fonte desconhecida',
            dataPublicacao: noticia.publishedAt, 
            favorito: jaFavoritado };
        })
      : [];

    const novasNoticiasProcessadas = novasNoticiasRaw.map(noticia => {
      const jaFavoritado = meusFavoritos.some(fav => fav.url === noticia.url);
      return { ...noticia, favorito: jaFavoritado };
    });

    noticias.value = [...noticias.value, ...novasNoticiasProcessadas];

    paginaAtual.value++;

    isLoggedIn.value = true;
  } catch (error) {
    console.error("Erro ao carregar feed:", error);
  } finally {
    carregandoMais.value=false;
  }
};

const toggleFavorito = async (noticia) => {
  const token = localStorage.getItem('token');
  noticia.favorito = !noticia.favorito;

  try {
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
      //Lógica de delete
      await axios.delete(`${API_URL}/favorites`, {
        headers: { Authorization: `Bearer ${token}` },
        data: { url: noticia.url, title: noticia.title }
      })
      console.log("Favorito removido do banco");
    }
  } catch (error) {
    console.error("Erro ao atualizar favorito:", error);
    noticia.favorito = !noticia.favorito;
    alert("Não foi possível atualizar o favorito");
  }
}

const modoAtual = ref('geral')

const alterarModoFeed = async (modo) => {
  modoAtual.value = modo

  noticias.value = []

  if (modo === 'favoritos') {
    noticias.value = favoritosLista.value.map(fav => ({
      title:fav.title,
      url: fav.url,
      urlToImage: fav.image_url || fav.urlToImage,
      favorito: true 
    }))
  } else if (modo === 'historico') {
    noticias.value = historicoLista.value.map(hist => {
      const jaFavoritado = favoritosLista.value.some(fav => fav.url === hist.url);

      return {
        id: hist.id,
        title: hist.title,
        url: hist.url,
        description: hist.description || 'Notícia acessada anteriormente.',
        urlToImage: hist.image_url || '',
        favorito: jaFavoritado
      }
    })
  } else {
    await carregarFeed({}, true)
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
      <TheHeader :verificandoAuth="verificandoAuth" @logout="logout" @toggle-menu="toggleSidebar" />

      <div class="content-layout" :class="{'sidebar-open':sidebarAberta}">
        
        <TheSidebar 
          :isOpen="sidebarAberta"
          @toggle="toggleSidebar"
          @mudar-feed="alterarModoFeed" 
        />

        <main class="main-content" style="width: 100%;">

          <h2 class="neon-text" style="text-transform: uppercase; margin: 20px 0; text-align: left;">
            {{ modoAtual === 'geral' ? 'Feed Principal' : `Feed de ${modoAtual}`}}
          </h2>
          
          <FilterBar @filter-change="carregarFeed" />

          <div class="feed-container">
            <template v-if="verificandoAuth">
              <SkeletonCard v-for="n in 6" :key="n" />
            </template>

            <template v-else>
              <template v-if="noticias.length > 0">
                <NewsCard 
                  v-for="(noticia, index) in noticias" 
                  :key="noticia.id || (noticia.url + '-' + index)" 
                  :item="noticia"
                  @toggle-fav="toggleFavorito"
                />
              </template>
              
              <div v-else class="empty-state neon-text-small" style="grid-column: 1 / -1; text-align: center; margin: 2rem;">
                Nenhuma notícia encontrada para essa busca ou filtro. Tente outra vez!
              </div>
            </template>
          </div>
        </main>
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

  .content-layout {
  display: flex; /* Coloca sidebar e conteúdo lado a lado */
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.main-content {
  flex: 1; /* Faz o feed ocupar todo o espaço restante */
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-layout {
  display: flex;
  transition: padding-left 0.3s ease; /* Transição suave do empurrão */
}

/* Se a sidebar estiver aberta, empurramos o conteúdo em telas grandes */
@media (min-width: 1024px) {
  .content-layout.sidebar-open {
    padding-left: 280px; 
  }
}
</style>