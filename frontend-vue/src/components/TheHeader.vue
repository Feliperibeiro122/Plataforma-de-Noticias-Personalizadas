<template>
  <header class="feed-header">
    <h1 class="neon-text">SEU FEED</h1>
    <button v-if="!verificandoAuth" @click="$emit('logout')" class="logout-btn">
      Sair
    </button>
  </header>
</template>

<script setup>
defineProps({
  verificandoAuth: Boolean
});
defineEmits(['logout']);
</script>

<style scoped>
.feed-header {
  display: grid; 
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 15px;
}

.feed-header h1 {
  grid-column: 2; 
  margin: 0;
  font-size: 1.5rem;
  text-align: center;
  color: var(--primary);
  letter-spacing: 1px;
}

.logout-btn {
  grid-column: 3;
  justify-self: end;
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
  margin-top: 0;
}

.logout-btn:hover {
  background: transparent;
  color: #ff4d4d;
  box-shadow: 0 0 20px rgba(255, 77, 77, 0.6);
  transform: scale(1.05);
}

@media (max-width: 870px) {
  .feed-header {
    display: flex;        
    flex-direction: column; 
    gap: 15px;            
    padding: 10px;
  }
  .feed-header h1 { font-size: 1.2rem; }
  .logout-btn { align-self: center; margin-top: 5px; }
}

@media (min-width: 601px) and (max-width: 1024px) {
  .feed-header {
    display: flex;
    justify-content: space-between; 
    padding: 0 30px;
  }
  .feed-header h1 {
    flex: 1;
    text-align: left; 
    font-size: 1.3rem;
    margin-right: 20px; 
  }
  .logout-btn {
    flex-shrink: 0;   
    margin-right: 20px;
  }
}
</style>