from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    preferences = Column(String, default="tecnologia")# Salvaremos as categorias separadas por vírgula

    history = relationship("History", back_populates="owner")
    favorites = relationship("Favorite", back_populates="owner")
    # --- TABELAS DOS DIFERENCIAIS (OPCIONAIS DO EDITAL) ---

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True,index=True)
    
    title = Column(String)
    url = Column(String)
    image_url = Column(String, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="favorites")

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    url = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    #Relacionamento: O histórico pertence a um usuário
    owner = relationship("User", back_populates="history")