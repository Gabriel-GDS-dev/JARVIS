# ============================================================
# app/models/memory.py
# Tabela de memórias persistentes do usuário
# ============================================================

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.core.database import Base


class Memory(Base):
    """
    Armazena informações importantes do usuário de forma persistente.
    
    Exemplos:
    - "O usuário prefere respostas curtas" (tipo: preferencia)
    - "O usuário está aprendendo Python" (tipo: fato)
    - "Estudar FastAPI até sexta-feira" (tipo: tarefa)
    """
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)                    # texto da memória
    memory_type = Column(String(50), default="fato")         # tipo da memória
    relevance = Column(Float, default=1.0)                   # relevância (0.0 a 1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Memory id={self.id} type='{self.memory_type}' content='{self.content[:50]}'>"
