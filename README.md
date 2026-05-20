# Plataforma de Notícias Personalizadas 

Aplicação full-stack desenvolvida como solução para o teste técnico da Trackland. O sistema consiste em um agregador de notícias com estética Cyberpunk/Neon que consome a NewsAPI, oferecendo uma experiência customizada de acordo com os interesses salvos de cada usuário.

## 🛠️ Tecnologias Utilizadas

* **Backend:** FastAPI (Python 3.12)
* **Banco de Dados:** SQLite com SQLAlchemy (Persistência robusta de dados)
* **Segurança:** Passlib (Hashing de senhas com bcrypt), PyJWT (Autenticação via Token JWT) e Python-dotenv
* **Frontend:** Vue.js 3 (Options/Composition API) & Axios
* **API Externa:** NewsAPI

## 📁 Estrutura do Projeto

```text
/
├── backend/            # API e lógica de negócio
│   ├── main.py         # Ponto de entrada, rotas e regras do feed
│   ├── models.py       # Modelagem do banco de dados (User, Favorites, History)
│   ├── schemas.py      # Esquemas de validação Pydantic
│   └── database.py     # Configuração do SQLAlchemy/SQLite
│   └── services.py     
├── frontend/           # Interface do usuário (Vue.js)
│   ├── src/
│   │   ├── components/ # Componentes (NewsCard, FilterBar, TheSidebar, etc.)
│   │   └── App.vue     # Componente principal e gerenciamento de estado
│   ├── package.json    # Dependências do ecossistema Node/Vue
│   └── vite.config.js  # Configuração do bundler Vite
└── README.md           # Documentação do projeto

Como Executar
1. Clonar o Repositório
git clone [https://github.com/Feliperibeiro122/Plataforma-de-Noticias-Personalizadas](https://github.com/Feliperibeiro122/Plataforma-de-Noticias-Personalizadas)
cd Plataforma-de-Noticias-Personalizadas

2. Configurar o Backend
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows (PowerShell):
./venv/Scripts/activate
# No Linux/macOS:
source venv/bin/activate

# Instalar as dependências do ecossistema Python
pip install -r requirements.txt

# Iniciar o servidor FastAPI
cd backend
uvicorn main:app --reload

# Iniciar o servidor do Vue
cd frontend

# Instalar dependências do Node.js
npm install

# Iniciar a aplicação em modo de desenvolvimento
npm run dev

Acesse o painel no endereço local fornecido pelo Vite (geralmente http://localhost:5173)

Acesse a documentação interativa em: http://127.0.0.1:8000/docs

⚡ Funcionalidades Implementadas
[x] Autenticação Segura: Sistema de Cadastro e Login de usuários utilizando criptografia de senhas (hashing) e persistência de sessão via tokens JWT.

[x] Gerenciamento de Interesses: Painel dinâmico na Barra Lateral que permite ao usuário cadastrar, ler e editar suas categorias de interesse a qualquer momento, persistindo as mudanças direto no SQLite.

[x] Feed Customizado: Exibição estruturada de notícias consumidas em tempo real utilizando os interesses do perfil logado.

[x] Tratamento de Estado Vazio: Tratamento de interface dinâmico usando tags estruturais do Vue para exibir mensagens amigáveis e centralizadas quando buscas não retornam resultados.

[x] Filtros Avançados: Barra de ferramentas capaz de aplicar filtros por palavras-chave e categorias combinadas.

[x] Paginação com Rolagem Infinita: Scroll inteligente automatizado que detecta a rolagem da página e requisita novos lotes de notícias de forma contínua, prevenindo loops em cenários sem registros.

[x] Sistema de Favoritos (Diferencial): Permite salvar e remover notícias prediletas com persistência total no banco de dados e aba dedicada no painel.

[x] Histórico de Leitura Automatizado (Diferencial): Armazena de forma cronológica as matérias visitadas pelo usuário, tratando e mitigando duplicidades caso o mesmo link seja aberto de forma recorrente.

Implementação de Filtros Avançados e Limitações da API
O sistema foi projetado com suporte arquitetural para cobrir filtros de Categoria, Palavra-Chave, Fonte e Período. Contudo, foram aplicadas regras de negócio específicas baseadas nas diretrizes de consumo da NewsAPI:

Restrições de Origem: A NewsAPI determina que a filtragem por fontes específicas (sources) ou períodos cronológicos estritos (from/to) seja executada majoritariamente sobre o endpoint global /everything. Além disso, a documentação veda expressamente a combinação do parâmetro de categorias simultaneamente com fontes no endpoint de manchetes principais (/top-headlines).

Decisão Arquitetural: Para priorizar a estabilidade do feed principal, o tempo de resposta e a paginação por rolagem infinita, a interface atual consome o endpoint de manchetes, consolidando a busca textual flexível por palavras-chave e categorias dinâmicas. Os parâmetros de data e fontes permanecem mapeados na estrutura do código do front-end prontos para expansão de escopo.
