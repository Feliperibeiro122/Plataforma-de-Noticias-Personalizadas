<template>
  <div class="news-card">
    <h3 class="neon-text-small">{{ item.title }}</h3>
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