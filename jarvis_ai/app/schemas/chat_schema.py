# ============================================================
# app/schemas/chat_schema.py
# Schemas Pydantic — validam dados de entrada e saída da API
# ============================================================

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# --- Schemas de Mensagem ---

class MessageBase(BaseModel):
    role: str
    content: str


class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # permite criar a partir de objetos SQLAlchemy


# --- Schemas de Conversa ---

class ConversationCreate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Schemas de Chat (endpoint principal) ---

class ChatRequest(BaseModel):
    """Corpo da requisição para o endpoint /chat"""
    message: str = Field(..., min_length=1, max_length=5000, description="Mensagem do usuário")
    conversation_id: Optional[int] = Field(None, description="ID da conversa. Se None, cria uma nova.")


class ChatResponse(BaseModel):
    """Resposta do endpoint /chat"""
    reply: str                        # resposta do modelo
    conversation_id: int              # ID da conversa (nova ou existente)
    message_id: int                   # ID da mensagem salva no banco
