from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    preferences = Column(String, default="")# Salvaremos as categorias separadas por vírgula

    # --- TABELAS DOS DIFERENCIAIS (OPCIONAIS DO EDITAL) ---

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tittle = Column(String)
    url = Column(String)
    source = Column(String)

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    viewed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))