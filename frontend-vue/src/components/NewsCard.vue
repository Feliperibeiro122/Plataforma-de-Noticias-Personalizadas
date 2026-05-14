<template>
  <div class="news-card">
    <h3 class="neon-text-small">{{ item.title }}</h3>
    <p>{{ item.description }}</p>

    <div class="card-actions">
      <a :href="item.url" target="_blank" class="read-more">Ler notícia</a>
      <button @click="$emit('toggle-fav', item)" class="fav-btn">
        {{ item.favorito ? '⭐' : '☆' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: Object
});
defineEmits(['toggle-fav']);
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