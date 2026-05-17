<template>
    <div class="filter-wrapper">
        <div class="search-box">
            <input
                type="text"
                v-model = "searchQuery"
                placeholder="Pesquisar notícias..."
                @keyup.enter="emitirFiltro"
            >
            <button @click="emitirFiltro" class="search-btn">🔍︎​</button>
        </div>

        <div class="tags-container">
            <button
                v-for="tag in tags"
                :key="tag"
                :class="['tag-btn', { active: selectedCategory === tag.toLowerCase() || (tag === 'Geral' && selectedCategory === '') }]"
                @click="selecionarTag(tag)"
            >
                {{ tag }}
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const searchQuery = ref('');
const selectedCategory = ref('')
const tags = ['Geral', 'Tech', 'Games', 'Science', 'Health'];

const emit = defineEmits(['filter-change']);

const emitirFiltro = () => {
    emit('filter-change', {
        search: searchQuery.value,
        category: selectedCategory.value
    });
};

const selecionarTag = (tag) => {
    // Se clicar na tag que já está selecionada ou em 'Geral', limpa o filtro
    if (selectedCategory.value === tag || tag === 'Geral') {
        selectedCategory.value = '';
    } else {
        selectedCategory.value = tag.toLowerCase();
    }
    emitirFiltro();
};
</script>

<style scoped>
.filter-wrapper {
    width: 100%;
    max-width: 1200px;
    margin-bottom: 30px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.search-box{
    display: flex;
    gap: 10px;
}

.search-box input{
    margin: 0;
    flex: 1;
}

.search-btn {
    width: auto;
    margin: 0;
    padding: 0 20px;
}

.tags-container {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 10px;
}

.tags-container::-webkit-scrollbar-thumb{
    background: var(--primary);
    border-radius: 10px;
}

.tag-btn{
    width: auto;
    margin: 0;
    padding: 8px 16px;
    background: var(--card);
    border: 1px solid #334155;
    color: #94a3b8;
    border-radius: 20px;
    white-space: nowrap;
    font-size: 0.85rem;
    transition: all 0.3 ease;
}

.tag-btn.active {
    background: transparent;
    color: var(--primary);
    border-color: var(--primary);
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}

.tag-btn:hover{
    border-color: var(--primary);
    color: white;
}
</style>