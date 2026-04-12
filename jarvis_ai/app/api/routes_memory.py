# ============================================================
# app/api/routes_memory.py
# Endpoints para gerenciar memórias do usuário
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.memory_schema import MemoryCreate, MemoryUpdate, MemoryResponse
from app.services.memory_service import memory_service

router = APIRouter(prefix="/memory", tags=["Memória"])


@router.post("/", response_model=MemoryResponse, status_code=201)
def create_memory(data: MemoryCreate, db: Session = Depends(get_db)):
    """
    Salva uma nova memória.
    
    Exemplo:
        POST /memory/
        {
            "content": "O usuário prefere respostas curtas e diretas",
            "memory_type": "preferencia",
            "relevance": 0.9
        }
    """
    return memory_service.create(db, data)


@router.get("/", response_model=List[MemoryResponse])
def list_memories(limit: int = 50, db: Session = Depends(get_db)):
    """Lista todas as memórias salvas, ordenadas por relevância."""
    return memory_service.get_all(db, limit=limit)


@router.get("/{memory_id}", response_model=MemoryResponse)
def get_memory(memory_id: int, db: Session = Depends(get_db)):
    """Retorna uma memória específica pelo ID."""
    memory = memory_service.get_by_id(db, memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memória não encontrada.")
    return memory


@router.put("/{memory_id}", response_model=MemoryResponse)
def update_memory(memory_id: int, data: MemoryUpdate, db: Session = Depends(get_db)):
    """Atualiza o conteúdo ou tipo de uma memória."""
    memory = memory_service.update(db, memory_id, data)
    if not memory:
        raise HTTPException(status_code=404, detail="Memória não encontrada.")
    return memory


@router.delete("/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    """Deleta uma memória pelo ID."""
    deleted = memory_service.delete(db, memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memória não encontrada.")
    return {"message": f"Memória {memory_id} deletada com sucesso."}
