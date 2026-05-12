from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models 
import schemas
from database import engine, get_db

# Configuração para criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(tittle="Trackland News API")

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar se o e-mail já existe
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # 2. Criptografar a senha
    hashed_password = pwd_context.hash(user.password)

    #Criar o objeto do usuário
    new_user = models.User(
        email = user.email,
        hashed_password=hashed_password
    )

    #4 Salvar no Banco
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/")
def home():
    return{"status": "API Online", "message": "Bem-vindo à Plataforma de Notícias"}