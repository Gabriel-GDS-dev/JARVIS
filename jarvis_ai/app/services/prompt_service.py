# ============================================================
# app/services/prompt_service.py
# Monta o prompt completo enviado ao modelo (contexto + histórico + memórias)
# ============================================================

from typing import List, Dict
from sqlalchemy.orm import Session
from app.core.constants import SYSTEM_PROMPT, ROLE_SYSTEM, ROLE_USER, ROLE_ASSISTANT
from app.core.config import settings
from app.models.chat import Message
from app.services.memory_service import memory_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PromptService:
    """
    Responsável por montar a lista de mensagens enviada ao LLM.
    
    Estrutura do prompt:
    1. [system] Instrução base + personalidade + memórias
    2. [user/assistant] Histórico recente da conversa
    3. [user] Mensagem atual do usuário
    """

    def build_messages(
        self,
        db: Session,
        user_message: str,
        history: List[Message],
    ) -> List[Dict[str, str]]:
        """
        Constrói a lista de mensagens para enviar ao Ollama.
        
        Args:
            db: Sessão do banco de dados
            user_message: Mensagem atual do usuário
            history: Histórico de mensagens da conversa
        
        Returns:
            Lista de dicts no formato esperado pelo Ollama
        """
        messages = []

        # 1. System prompt com personalidade e memórias
        memories_text = memory_service.get_context_memories(db)
        system_content = SYSTEM_PROMPT.format(
            name=settings.jarvis_name,
            memories=memories_text,
        )
        messages.append({"role": ROLE_SYSTEM, "content": system_content})

        # 2. Histórico recente (limitado para não estourar o contexto)
        recent_history = history[-settings.max_history_messages:]
        for msg in recent_history:
            messages.append({"role": msg.role, "content": msg.content})

        # 3. Mensagem atual do usuário
        messages.append({"role": ROLE_USER, "content": user_message})

        logger.info(
            f"📋 Prompt montado: {len(messages)} mensagens "
            f"(1 system + {len(recent_history)} histórico + 1 atual)"
        )

        return messages


# Instância global
prompt_service = PromptService()
