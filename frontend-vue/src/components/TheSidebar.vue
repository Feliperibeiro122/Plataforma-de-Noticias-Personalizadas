<template>
  <div>
    <div v-if="isOpen" class="sidebar-overlay" @click="$emit('toggle')"></div>

    <aside :class="['sidebar-drawer', { 'is-open': isOpen }]">
      <button class="toggle-btn" @click="$emit('toggle')">
        <span class="icon">{{ isOpen ? '✕' : '☰' }}</span>
      </button>
      
      <div class="sidebar-content" v-show="isOpen">
        <h3 class="section-title">⭐ Favoritos</h3>
        <ul class="sidebar-list">
          <li v-for="fav in favoritos" :key="fav.url" class="sidebar-item">
            <a :href="fav.url" target="_blank" class="sidebar-link">{{ fav.title }}</a>
          </li>
        </ul>

        <hr class="divider" />

        <h3 class="section-title">🕒 Histórico</h3>
        <ul class="sidebar-list">
          <li v-for="item in historico" :key="item.url" class="sidebar-item">
            <a :href="item.url" target="_blank" class="sidebar-link history-link">{{ item.title }}</a>
          </li>
        </ul>
      </div>
    </aside>
  </div>
</template>

<script setup>
defineProps(['favoritos', 'historico', 'isOpen']);
defineEmits(['toggle']);
</script>

<style scoped>
.sidebar-drawer {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 0; /* Largura zero quando fechada */
  background: #1e293b;
  z-index: 1000;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-right: none;
  overflow: visible; /* Permite que o botão saia para fora */
}

.sidebar-drawer.is-open {
  width: 280px; /* Largura total quando aberta */
  border-right: 2px solid var(--primary);
  padding: 20px;
}

/* BOTÃO FLUTUANTE DISCRETO */
.toggle-btn {
  position: absolute;
  top: 15px;
  right: -50px; /* Sempre fica à direita da borda da barra */
  width: 40px;
  height: 40px;
  background: var(--card);
  border: 1px solid #334155;
  border-radius: 50%; /* Redondo para não parecer um "caroço" */
  color: var(--primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  transition: all 0.3s ease;
}

.sidebar-drawer.is-open .toggle-btn {
  right: 15px; /* Pula para dentro da barra quando aberta */
  background: transparent;
  border-color: transparent;
}

.toggle-btn:hover {
  transform: scale(1.1);
  border-color: var(--primary);
}

.sidebar-content {
  opacity: 0;
  transition: opacity 0.2s ease;
  white-space: nowrap; /* Evita que o texto quebre enquanto a barra abre */
}

.sidebar-drawer.is-open .sidebar-content {
  opacity: 1;
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  z-index: 999;
}

@media (max-width: 768px) {
  .sidebar-drawer.is-open {
    width: 50vw; /* Ocupa quase tudo no mobile */
  }
}
</style>