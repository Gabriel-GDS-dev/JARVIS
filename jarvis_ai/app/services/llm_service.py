# ============================================================
# app/services/llm_service.py
# Responsável por toda comunicação com o Ollama
# ============================================================

import requests
from typing import List, Dict
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    """
    Serviço que encapsula a comunicação com o Ollama.
    
    Toda a lógica de chamada ao modelo fica AQUI.
    Se você quiser trocar de modelo ou de provider no futuro,
    só precisa alterar este arquivo.
    """

    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.chat_url = f"{self.base_url}/api/chat"
        self.generate_url = f"{self.base_url}/api/generate"

    def check_connection(self) -> bool:
        """
        Verifica se o Ollama está rodando e acessível.
        Retorna True se OK, False se houver erro.
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            logger.error("❌ Ollama não está rodando. Execute: ollama serve")
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao conectar no Ollama: {e}")
            return False

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Envia uma lista de mensagens ao Ollama e retorna a resposta.
        
        Args:
            messages: Lista de dicts no formato:
                      [{"role": "system", "content": "..."},
                       {"role": "user", "content": "..."},
                       {"role": "assistant", "content": "..."}]
        
        Returns:
            String com a resposta do modelo.
        
        Raises:
            ConnectionError: Se o Ollama não estiver acessível.
            RuntimeError: Para outros erros da API.
        """
        if not self.check_connection():
            raise ConnectionError(
                "O Ollama não está rodando. "
                "Execute 'ollama serve' no terminal e tente novamente."
            )

        try:
            logger.info(f"🤖 Enviando {len(messages)} mensagens para o modelo '{self.model}'")

            response = requests.post(
                self.chat_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,          # False = espera resposta completa
                    "options": {
                        "temperature": 0.7,   # criatividade (0.0 = determinístico, 1.0 = criativo)
                        "num_predict": 1024,  # máximo de tokens na resposta
                    }
                },
                timeout=120,  # aguarda até 2 minutos
            )

            response.raise_for_status()
            data = response.json()

            reply = data["message"]["content"]
            logger.info(f"✅ Resposta recebida ({len(reply)} caracteres)")
            return reply

        except requests.exceptions.Timeout:
            raise RuntimeError("O modelo demorou muito para responder. Tente uma pergunta mais simples.")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"Erro na API do Ollama: {e.response.status_code} - {e.response.text}")
        except KeyError:
            raise RuntimeError("Resposta inesperada do Ollama. Verifique se o modelo está instalado.")
        except Exception as e:
            logger.error(f"Erro inesperado no LLMService: {e}")
            raise RuntimeError(f"Erro ao gerar resposta: {str(e)}")


# Instância global — importe isso nos outros serviços
llm_service = LLMService()
