<template>
  <div class="news-card">
    <h3 class="neon-text-small">{{ item.title }}</h3>

    <div class="news-meta" style="font-size: 0.8rem; color: #888;margin-bottom: 10px;">
      <span class="source">📰 {{ item.fonte || item.source?.name }}</span>
      <span class="date">📅 {{ formatarData(item.dataPublicacao || item.publishedAt) }}</span>
    </div>

    <p>{{ item.description }}</p>

    <div class="card-actions">
      <a :href="item.url" target="_blank" class="read-more" @click="registrarNoHistorico">Ler notícia</a>
      <button @click="$emit('toggle-fav', item)" class="fav-btn">
        {{ item.favorito ? '⭐' : '☆' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';

const props = defineProps({
  item: Object
});
defineEmits(['toggle-fav']);

const API_URL = 'http://localhost:8000';

// Registro das notícias lidas no histórico
const registrarNoHistorico = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) return;

    await axios.post(`${API_URL}/history`, {
      title: props.item.title,
      url: props.item.url
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    console.log("Notícia registrada no histórico com sucesso!");
  } catch(error) {
    console.error("Erro ao registrar no histórico:", error);
  }
}

const formatarData = (dataIso) => {
  if (!dataIso) return '';
  const data = new Date(dataIso);
  return data.toLocaleDateString('pt-BR');
}
</script>

<style scoped>
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
  width: auto; 
  padding: 5px;
  margin: 0;
  font-size: 1.2rem;
  border: none;
  color: white;
  cursor: pointer;
}
</style>