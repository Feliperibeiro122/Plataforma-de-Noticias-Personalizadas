from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# O que o usuário envia no cadastro
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    preferences: str = "tecnologia"

# O que a API devolve (não devolvemos a senha!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    preferences: Optional[str] = None

    class Config:
        from_attributes = True
    
class UserPreferences(BaseModel):
    categories: list[str]

class Token(BaseModel):
    acess_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None

class HistoryBase(BaseModel):
    title: str
    url: str

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    id:int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True