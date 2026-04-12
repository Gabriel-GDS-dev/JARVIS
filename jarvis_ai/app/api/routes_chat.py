# ============================================================
# app/api/routes_chat.py
# Endpoints relacionados ao chat com o Jarvis
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse, ConversationResponse
from app.services.assistant_service import assistant_service
from app.models.chat import Conversation, Message
from app.utils.logger import get_logger
from typing import List

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Endpoint principal — envia uma mensagem ao Jarvis e recebe a resposta.
    
    Body:
        message: texto da mensagem do usuário
        conversation_id: (opcional) ID de uma conversa existente
    
    Exemplo de uso:
        POST /chat/
        {
            "message": "Olá, tudo bem?",
            "conversation_id": null
        }
    """
    try:
        result = assistant_service.process_message(
            db=db,
            user_message=request.message,
            conversation_id=request.conversation_id,
        )
        return ChatResponse(**result)
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Erro inesperado no endpoint /chat: {e}")
        raise HTTPException(status_code=500, detail="Erro interno inesperado.")


@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(limit: int = 20, db: Session = Depends(get_db)):
    """
    Lista todas as conversas salvas, da mais recente para a mais antiga.
    """
    conversations = (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
        .all()
    )
    return conversations


@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    """
    Retorna todas as mensagens de uma conversa específica.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return {
        "conversation_id": conversation_id,
        "title": conversation.title,
        "messages": [
            {"id": m.id, "role": m.role, "content": m.content, "created_at": m.created_at}
            for m in messages
        ]
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma conversa e todas as suas mensagens.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")
    db.delete(conversation)
    db.commit()
    return {"message": f"Conversa {conversation_id} deletada com sucesso."}
