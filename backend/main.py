from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

import models 
import schemas
from database import engine, get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

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

@app.post("/login",response_model=schemas.Token)
def login(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Busca o usuário no banco pelo e-mail
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    #2. Se não achar usuário no banco
    if not user or not pwd_context.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )
    
    #4. Gera o Token
    token = create_acess_token(data={"sub": str(user.id)})

    #5. Retorna o Token único
    return {"acess_token":token, "token_type": "bearer"}


@app.put("/preferences/{user_id}")
def update_preferences(user_id: int, pref: schemas.UserPreferences, db: Session = Depends(get_db)):
    #1. Busca o usuário pelo ID
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    #2. Converte a lista em uma string
    preferences_string = ", ".join(pref.categories)

    #3. Atualiza o campo no banco
    db_user.preferences = preferences_string
    db.commit()
    db.refresh(db_user)

    return{"message": "Preferências atualizadas!", "preferences": db_user.preferences}

@app.get("/")
def home():
    return{"status": "API Online", "message": "Bem-vindo à Plataforma de Notícias"}