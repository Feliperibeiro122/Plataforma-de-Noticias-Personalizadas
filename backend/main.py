from fastapi import FastAPI, Depends, HTTPException
from fastapi import security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional


from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

import services
import models 
import schemas
from database import engine, get_db

load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
auth_scheme = HTTPBearer()

def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(models.User).filter(models.User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

# Configuração para criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(tittle="Trackland News API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],   # Em produção, vou colocar o link do site aqui
    allow_credentials = True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permite todos os cabeçalhos (como o de Autenticação)
)


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
        hashed_password=hashed_password,
        preferences=getattr(user, 'preferences', 'tecnologia')
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
    return {"access_token":token, "token_type": "bearer"}


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

@app.get("/feed")
def get_user_feed(
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: models.User = Depends(get_current_user)
):
    # 1. Define a lógica de busca direto no termo
    # Prioridade: 1º Busca manual, 2º Categoria/Tag, 3º Preferências vindas do banco
    termo_de_busca = search or category or current_user.preferences

    # 2. Chama o serviço de notícias criado
    noticias = services.fetch_news_by_preferences(termo_de_busca)

    return {
        "usuario": current_user.email,
        "filtro_aplicado": termo_de_busca,
        "noticias": noticias
    }

@app.post("/history", response_model=schemas.History)
def add_to_history(history_data: schemas.HistoryCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    #verificação de duplicata: Caso exista essa URL para x usuário, ela não será salva novamente
    already_exists = db.query(models.History).filter(
        models.History.user_id == current_user.id,
        models.History.url == history_data.url
    ).first()

    if already_exists:
        return already_exists
    
    new_history = models.History(
        title = history_data.title,
        url = history_data.url,
        user_id = current_user.id
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history

#2. Rota para listar o histórico do usuário logado
@app.get("/history", response_model=list[schemas.History])
def get_user_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    #Retorna o hitórico do mais recente para o mais antigo
    return db.query(models.History).filter(models.History.user_id == current_user.id).order_by(models.History.timestamp.desc()).all()

@app.post("/favorites", response_model=schemas.FavoriteResponse)
def add_favorite(
    favorite:schemas.FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) #Apenas para quem estiver logado
):
    #1. Cria o objeto do banco com o ID do usuário logado
    db_favorite = models.Favorite(
        **favorite.dict(),
        user_id = current_user.id
    )

    #2. Salva no banco
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)

    return db_favorite

#Rota para listar os favoritos do usuário logado
@app.get("/favorites", response_model=list[schemas.FavoriteResponse])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return current_user.favorites

@app.get("/")
def home():
    return{"status": "API Online", "message": "Bem-vindo à Plataforma de Notícias"}