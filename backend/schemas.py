from pydantic import BaseModel, EmailStr
from typing import Optional

# O que o usuário envia no cadastro
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# O que a API devolve (não devolvemos a senha!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    preferences: Optional[str] = None

    class Config:
        from_attributes = True
    
class UserPreferences(BaseModel):
    categories: list[str]