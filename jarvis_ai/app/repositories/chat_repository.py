# ============================================================
# app/repositories/chat_repository.py
# Camada de acesso a dados para conversas e mensagens
# Separa a lógica de banco do restante do código
# ============================================================

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.chat import Conversation, Message


class ChatRepository:
    """
    Responsável por todas as operações de banco de dados
    relacionadas a conversas e mensagens.
    """

    def create_conversation(self, db: Session, title: str = None) -> Conversation: # type: ignore
        conv = Conversation(title=title or "Nova conversa")
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv

    def get_conversation(self, db: Session, conversation_id: int) -> Optional[Conversation]:
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_all_conversations(self, db: Session, limit: int = 20) -> List[Conversation]:
        return (
            db.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .all()
        )

    def delete_conversation(self, db: Session, conversation_id: int) -> bool:
        conv = self.get_conversation(db, conversation_id)
        if not conv:
            return False
        db.delete(conv)
        db.commit()
        return True

    def add_message(self, db: Session, conversation_id: int, role: str, content: str) -> Message:
        msg = Message(conversation_id=conversation_id, role=role, content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    def get_messages(self, db: Session, conversation_id: int, limit: int = 100) -> List[Message]:
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
            .all()
        )


# Instância global
chat_repository = ChatRepository()
