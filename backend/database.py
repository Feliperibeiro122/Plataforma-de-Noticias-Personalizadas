from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Nome do arquivo do banco de dados que será criado automaticamente
SQLALCHEMY_DATABASE_URL = "sqlite:///./news_platform.db"

# O 'check_same_thread' é exigido pelo SQLite no FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para criar os modelos
Base = declarative_base()

# Função para abrir e fechar a conexão a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
