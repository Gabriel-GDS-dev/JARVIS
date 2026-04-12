# ============================================================
# app/schemas/memory_schema.py
# Schemas de entrada e saída para memórias
# ============================================================

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MemoryCreate(BaseModel):
    """Corpo para criar uma nova memória"""
    content: str = Field(..., min_length=1, max_length=2000)
    memory_type: str = Field(default="fato", description="Tipo: fato, preferencia, tarefa, nota")
    relevance: float = Field(default=1.0, ge=0.0, le=1.0)


class MemoryUpdate(BaseModel):
    """Corpo para atualizar uma memória existente"""
    content: Optional[str] = None
    memory_type: Optional[str] = None
    relevance: Optional[float] = None


class MemoryResponse(BaseModel):
    """Resposta com dados de uma memória"""
    id: int
    content: str
    memory_type: str
    relevance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
