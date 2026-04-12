# ============================================================
# app/services/memory_service.py
# Gerencia criação, leitura e uso das memórias do usuário
# ============================================================

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.memory import Memory
from app.schemas.memory_schema import MemoryCreate, MemoryUpdate
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryService:
    """
    Lida com toda a lógica de memórias:
    - Criar memórias a partir de comandos do usuário
    - Buscar memórias relevantes para o contexto
    - Atualizar e deletar memórias
    """

    def create(self, db: Session, data: MemoryCreate) -> Memory:
        """Cria uma nova memória no banco."""
        memory = Memory(
            content=data.content,
            memory_type=data.memory_type,
            relevance=data.relevance,
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)
        logger.info(f"💾 Memória criada: [{data.memory_type}] {data.content[:60]}")
        return memory

    def get_all(self, db: Session, limit: int = 50) -> List[Memory]:
        """Retorna todas as memórias, ordenadas por relevância."""
        return (
            db.query(Memory)
            .order_by(Memory.relevance.desc(), Memory.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, memory_id: int) -> Optional[Memory]:
        """Retorna uma memória pelo ID."""
        return db.query(Memory).filter(Memory.id == memory_id).first()

    def update(self, db: Session, memory_id: int, data: MemoryUpdate) -> Optional[Memory]:
        """Atualiza uma memória existente."""
        memory = self.get_by_id(db, memory_id)
        if not memory:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(memory, field, value)
        db.commit()
        db.refresh(memory)
        return memory

    def delete(self, db: Session, memory_id: int) -> bool:
        """Deleta uma memória. Retorna True se deletou, False se não encontrou."""
        memory = self.get_by_id(db, memory_id)
        if not memory:
            return False
        db.delete(memory)
        db.commit()
        logger.info(f"🗑️  Memória {memory_id} deletada")
        return True

    def get_context_memories(self, db: Session) -> str:
        """
        Retorna as memórias mais relevantes formatadas como texto,
        prontas para serem inseridas no prompt do sistema.
        """
        memories = (
            db.query(Memory)
            .order_by(Memory.relevance.desc())
            .limit(settings.max_memories_context)
            .all()
        )

        if not memories:
            return "Nenhuma memória salva ainda."

        lines = []
        for m in memories:
            lines.append(f"- [{m.memory_type.upper()}] {m.content}")

        return "\n".join(lines)


# Instância global
memory_service = MemoryService()
