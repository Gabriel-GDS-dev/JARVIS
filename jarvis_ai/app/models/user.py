# ============================================================
# app/models/user.py
# Tabela de perfil do usuário (para uso futuro com autenticação)
# ============================================================

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


class User(Base):
    """
    Perfil do usuário — atualmente apenas um usuário local.
    Preparado para evolução futura com múltiplos usuários.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, default="Usuário")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User id={self.id} name='{self.name}'>"
