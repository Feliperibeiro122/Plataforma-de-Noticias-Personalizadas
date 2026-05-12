from fastapi import FastAPI
import models
from database import engine

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(tittle="Trackland News API")

@app.get("/")
def home():
    return{"status": "API Online", "message": "Bem-vindo à Plataforma de Notícias"}