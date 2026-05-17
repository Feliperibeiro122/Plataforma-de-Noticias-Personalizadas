<template>
  <div>
    <div v-if="isOpen" class="sidebar-overlay" @click="$emit('toggle')"></div>

    <aside :class="['sidebar-drawer', { 'is-open': isOpen }]">
      <button class="toggle-btn" @click="$emit('toggle')">
        <span class="icon">{{ isOpen ? '✕' : '☰' }}</span>
      </button>
      
      <div class="sidebar-content" v-show="isOpen">
        <h2 class="sidebar-brand">Navegação</h2>
        
        <ul class="sidebar-menu">
          <li class="menu-item" @click="navegar('geral')">
            <span class="menu-icon">🏠︎</span> Home
          </li>

          <li class="menu-item" @click="navegar('favoritos')">
            <span class="menu-icon">☆</span> Meus Favoritos
          </li>

          <li class="menu-item" @click="navegar('historico')">
            <span class="menu-icon">↺</span> Histórico de Leitura
          </li>
        </ul>
      </div>
    </aside>
  </div>
</template>

<script setup>
defineProps(['isOpen']); // Não precisamos mais passar as listas de dados para cá
const emit = defineEmits(['toggle', 'mudar-feed']);

const navegar = (destino) => {
  emit('mudar-feed', destino); // Avisa o App.vue qual página carregar
  emit('toggle');              // Fecha a sidebar após o clique
}
</script>

<style scoped>
/* Mantém seus estilos anteriores (.sidebar-drawer, .toggle-btn, etc) */
.sidebar-drawer {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 0;
  background: #1e293b;
  z-index: 1000;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: visible;
}
.sidebar-drawer.is-open {
  width: 280px;
  border-right: 2px solid var(--primary);
  padding: 20px;
}
.toggle-btn {
  position: absolute;
  top: 15px;
  right: -50px;
  width: 40px;
  height: 40px;
  background: var(--card);
  border: 1px solid #334155;
  border-radius: 50%;
  color: var(--primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.sidebar-drawer.is-open .toggle-btn {
  right: 15px;
  background: transparent;
  border-color: transparent;
}
.sidebar-content {
  opacity: 0;
  transition: opacity 0.2s ease;
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

/* ESTILOS NOVOS PARA O MENU ESTILO YOUTUBE */
.sidebar-brand {
  font-size: 1.2rem;
  color: var(--primary);
  margin-bottom: 25px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}
.menu-item {
  display: flex;
  align-items: center;
  padding: 14px 12px;
  color: #f8fafc;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: background 0.2s, color 0.2s;
}
.menu-item:hover {
  background: #334155;
  color: var(--primary);
}
.menu-icon {
  margin-right: 15px;
  font-size: 1.2rem;
}
</style>