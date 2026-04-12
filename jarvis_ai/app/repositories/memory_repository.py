# ============================================================
# app/repositories/memory_repository.py
# Camada de acesso a dados para memórias
# ============================================================

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.memory import Memory


class MemoryRepository:

    def create(self, db: Session, content: str, memory_type: str, relevance: float = 1.0) -> Memory:
        memory = Memory(content=content, memory_type=memory_type, relevance=relevance)
        db.add(memory)
        db.commit()
        db.refresh(memory)
        return memory

    def get_by_id(self, db: Session, memory_id: int) -> Optional[Memory]:
        return db.query(Memory).filter(Memory.id == memory_id).first()

    def get_all(self, db: Session, limit: int = 50) -> List[Memory]:
        return (
            db.query(Memory)
            .order_by(Memory.relevance.desc(), Memory.created_at.desc())
            .limit(limit)
            .all()
        )

    def delete(self, db: Session, memory_id: int) -> bool:
        memory = self.get_by_id(db, memory_id)
        if not memory:
            return False
        db.delete(memory)
        db.commit()
        return True


# Instância global
memory_repository = MemoryRepository()
