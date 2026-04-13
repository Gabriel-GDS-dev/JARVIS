# ============================================================
# app/services/assistant_service.py
# Orquestrador principal — conecta todos os serviços
# ============================================================

from sqlalchemy.orm import Session
from app.models.chat import Conversation, Message
from app.schemas.memory_schema import MemoryCreate
from app.services.llm_service import llm_service
from app.services.prompt_service import prompt_service
from app.services.memory_service import memory_service
from app.core.constants import ROLE_USER, ROLE_ASSISTANT
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


# Comandos internos que o usuário pode digitar
INTERNAL_COMMANDS = {
    "salvar memória": "save_memory",
    "salve como memória": "save_memory",
    "salvar isso": "save_memory",
    "mostrar memórias": "list_memories",
    "listar memórias": "list_memories",
    "minhas memórias": "list_memories",
}


class AssistantService:
    """
    Ponto central da lógica do Jarvis.
    
    Fluxo de uma mensagem:
    1. Recebe a mensagem do usuário
    2. Verifica se é um comando interno
    3. Busca ou cria a conversa
    4. Carrega o histórico
    5. Monta o prompt completo
    6. Chama o LLM
    7. Salva a conversa no banco
    8. Retorna a resposta
    """

    def process_message(
        self,
        db: Session,
        user_message: str,
        conversation_id: int = None, # type: ignore
    ) -> dict:
        """
        Processa uma mensagem do usuário e retorna a resposta do Jarvis.
        
        Args:
            db: Sessão do banco
            user_message: O que o usuário digitou
            conversation_id: ID da conversa existente (None = nova conversa)
        
        Returns:
            dict com: reply, conversation_id, message_id
        """

        # --- Verifica comandos internos ---
        command_response = self._check_internal_command(db, user_message)
        if command_response:
            # Salva no histórico mesmo sendo comando interno
            conv_id = conversation_id or self._get_or_create_conversation(db).id
            msg = self._save_message(db, conv_id, ROLE_USER, user_message) # type: ignore
            self._save_message(db, conv_id, ROLE_ASSISTANT, command_response) # type: ignore
            return {"reply": command_response, "conversation_id": conv_id, "message_id": msg.id}

        # --- Busca ou cria conversa ---
        if conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if not conversation:
                logger.warning(f"Conversa {conversation_id} não encontrada. Criando nova.")
                conversation = self._get_or_create_conversation(db)
        else:
            conversation = self._get_or_create_conversation(db, title=user_message[:50])

        # --- Carrega histórico ---
        history = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
            .all()
        )

        # --- Monta o prompt ---
        messages = prompt_service.build_messages(
            db=db,
            user_message=user_message,
            history=history,
        )

        # --- Chama o modelo ---
        reply = llm_service.chat(messages)

        # --- Salva as mensagens no banco ---
        user_msg = self._save_message(db, conversation.id, ROLE_USER, user_message) # type: ignore
        self._save_message(db, conversation.id, ROLE_ASSISTANT, reply) # type: ignore

        logger.info(f"💬 Conversa {conversation.id} | Mensagem {user_msg.id} processada")

        return {
            "reply": reply,
            "conversation_id": conversation.id,
            "message_id": user_msg.id,
        }

    def _get_or_create_conversation(self, db: Session, title: str = None) -> Conversation: # type: ignore
        """Cria uma nova conversa no banco."""
        conversation = Conversation(title=title or "Nova conversa")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def _save_message(
        self, db: Session, conversation_id: int, role: str, content: str
    ) -> Message:
        """Salva uma mensagem no banco de dados."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def _check_internal_command(self, db: Session, message: str) -> str | None:
        """
        Verifica se a mensagem é um comando interno do Jarvis.
        Retorna a resposta do comando ou None se não for um comando.
        """
        msg_lower = message.lower().strip()

        # Comando: listar memórias
        if any(cmd in msg_lower for cmd in ["mostrar memórias", "listar memórias", "minhas memórias"]):
            memories = memory_service.get_all(db)
            if not memories:
                return "Você ainda não tem memórias salvas."
            lines = [f"Aqui estão suas memórias salvas:\n"]
            for m in memories:
                lines.append(f"• [{m.memory_type}] {m.content}")
            return "\n".join(lines)

        # Comando: salvar memória (a próxima parte da mensagem é o conteúdo)
        save_triggers = ["salvar memória:", "salve como memória:", "salvar isso:"]
        for trigger in save_triggers:
            if msg_lower.startswith(trigger):
                content = message[len(trigger):].strip()
                if content:
                    memory_service.create(db, MemoryCreate(content=content))
                    return f"✅ Memória salva: \"{content}\""
                return "Por favor, informe o que deseja salvar após o comando."

        return None  # não é um comando interno


# Instância global
assistant_service = AssistantService()
