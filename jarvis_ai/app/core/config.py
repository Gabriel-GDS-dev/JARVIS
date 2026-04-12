# ============================================================
# app/core/config.py
# Configurações centrais do projeto — lidas do arquivo .env
# ============================================================

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Todas as configurações do Jarvis são lidas aqui.
    Os valores padrão são usados se a variável não estiver no .env
    """

    # Nome da IA
    jarvis_name: str = "Jarvis"

    # Ollama
    ollama_model: str = "llama3"
    ollama_base_url: str = "http://localhost:11434"

    # Banco de dados
    database_url: str = "sqlite:///./data/app.db"

    # Ambiente
    environment: str = "development"

    # Porta da API
    api_port: int = 8000

    # Contexto
    max_history_messages: int = 20
    max_memories_context: int = 10

    class Config:
        # Diz ao Pydantic para ler o arquivo .env
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna as configurações. O @lru_cache garante que o .env
    é lido apenas uma vez durante a execução do app.
    """
    return Settings()


# Instância global de configurações — importe isso em outros módulos
settings = get_settings()
