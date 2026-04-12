# ============================================================
# app/api/routes_health.py
# Endpoints de verificação de saúde da aplicação
# ============================================================

from fastapi import APIRouter
from app.services.llm_service import llm_service
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """
    Verifica se a API está funcionando.
    Sempre retorna 200 OK se a API estiver de pé.
    
    Use este endpoint para confirmar que o servidor iniciou corretamente.
    """
    return {"status": "ok", "message": "Jarvis AI está funcionando!"}


@router.get("/status")
def full_status():
    """
    Verifica o status completo do sistema:
    - API: sempre OK se este endpoint responder
    - Ollama: verifica se o modelo local está acessível
    """
    ollama_ok = llm_service.check_connection()

    return {
        "api": "ok",
        "ollama": "ok" if ollama_ok else "offline",
        "model": settings.ollama_model,
        "jarvis_name": settings.jarvis_name,
        "environment": settings.environment,
        "tips": (
            None if ollama_ok
            else "Execute 'ollama serve' no terminal para ativar o modelo local."
        )
    }
