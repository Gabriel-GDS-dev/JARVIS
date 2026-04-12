# ============================================================
# app/models/chat.py
# Tabelas do banco de dados para conversas e mensagens
# ============================================================

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Conversation(Base):
    """
    Representa uma sessão de conversa completa.
    Uma conversa contém várias mensagens.
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)           # título opcional da conversa
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento: uma conversa tem muitas mensagens
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation id={self.id} title='{self.title}'>"


class Message(Base):
    """
    Representa uma mensagem individual dentro de uma conversa.
    Pode ser do usuário ('user') ou do assistente ('assistant').
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)             # 'user' ou 'assistant'
    content = Column(Text, nullable=False)               # conteúdo da mensagem
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamento inverso
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message id={self.id} role='{self.role}' conv={self.conversation_id}>"
