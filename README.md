Plataforma de Notícias Personalizadas

    Aplicação full-stack desenvolvida para o teste técnico da Trackland. O sistema permite que usuários acompanhem notícias baseadas em seus interesses através da integração com APIs públicas.

Tecnologias Utilizadas
    Backend: FastAPI (Python 3.12).
    Banco de Dados: SQLite com SQLAlchemy (Persistência de dados).
    Segurança: Passlib (Hashing de senhas) e Python-dotenv (Gestão de chaves de API).
    Frontend: Vue.js / React / Next.js.
    API Externa: NewsAPI.  

 Estrutura do Projeto
 /
├── backend/            # API e lógica de negócio
│   ├── main.py         # Ponto de entrada e rotas
│   ├── models.py       # Modelagem do banco de dados (User, Prefs, Fav)
│   ├── database.py     # Configuração do SQLAlchemy/SQLite
│   └── .env            # Variáveis de ambiente (Chaves de API)
├── frontend/           # Interface do usuário
├── requirements.txt    # Dependências do Python
└── README.md           # Documentação

Como Executar
1. Clonar o Repositório
git clone https://github.com/Feliperibeiro122/Plataforma-de-Noticias-Personalizadas
cd nome-do-repo

2. Configurar o Backend
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# No Windows (powershell):
./venv/Scripts/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
cd backend
uvicorn main:app --reload

Acesse a documentação interativa em: http://127.0.0.1:8000/docs

Funcionalidades Implementadas
[x] Cadastro e Login de Usuários com senha criptografada.  

[x] Seleção de categorias de interesse (Tecnologia, Esportes, etc.).  

[ ] Feed de notícias filtrado por preferências (Em desenvolvimento).  

[ ] Sistema de Favoritos (Diferencial).  

[ ] Histórico de Leitura sem duplicidade (Diferencial).