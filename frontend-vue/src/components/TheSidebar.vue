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

          <div class="sidebar-preferences" style="margin-top: 30px; padding: 15px; border-top: 1px solid #334155;">
            <h3 style="font-size: 0.9rem; color: #4ef2d2; margin-bottom: 10px; text-transform: uppercase;">Minhas Preferências</h3>

            <input 
              type="text" 
              v-model="novasPrefs" 
              placeholder="Ex: tech, games, science"
              style="font-size: 0.85rem; padding: 8px; margin-bottom: 10px;"
            />
            
            <button 
              @click="salvarPreferencias" 
              style="padding: 8px; font-size: 0.85rem; background: #6366f1;"
            >
              Salvar Interesses
            </button>
          </div>
        </ul>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const novasPrefs = ref('')
const API_URL = "http://127.0.0.1:8000"

const salvarPreferencias = async () => {
  const token = localStorage.getItem('token')

  if (!token) {
    alert("Usuário não autenticado. Faça login novamente.")
    return
  }

  let userId = null
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const payloadJson = JSON.parse(window.atob(base64))
    
    userId = payloadJson.sub || payloadJson.user_id
  } catch (e) {
    console.error("Erro ao decodificar o token:", e)
  }

  // Se mesmo assim não achar o ID, tenta o plano B do localStorage
  if (!userId) {
    userId = localStorage.getItem('userId')
  }

  // Se ainda for nulo, avisa o usuário
  if (!userId) {
    alert("Não foi possível identificar usuário.")
    return
  }

  if (!novasPrefs.value.trim()) {
    alert("Digite pelo menos uma preferência!")
    return
  }

  // Trata o texto digitado transformando em Array
  const listaCategorias = novasPrefs.value
    .split(',')
    .map(item => item.trim())
    .filter(item => item !== '')

  try {
    // Dispara o PUT com o ID numérico correto extraído do Token
    const response = await axios.put(
      `${API_URL}/preferences/${parseInt(userId, 10)}`, 
      { categories: listaCategorias }, 
      { headers: { Authorization: `Bearer ${token}` } }
    )
    
    alert("Preferências atualizadas com sucesso! 🎉")
  } catch (error) {
    console.error("Erro ao salvar preferências:", error)
    alert(error.response?.data?.detail || "Erro 422: Verifique o formato enviado.")
  }
}

defineProps(['isOpen']);
const emit = defineEmits(['toggle', 'mudar-feed']);

const navegar = (destino) => {
  emit('mudar-feed', destino); // Avisa o App.vue qual página carregar
  emit('toggle');              // Fecha a sidebar após o clique
}
</script>

<style scoped>
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