# ============================================================
# app/utils/logger.py
# Logger centralizado para todo o projeto
# ============================================================

import logging
import os
from datetime import datetime

# Garante que a pasta de logs existe
os.makedirs("data/logs", exist_ok=True)

# Nome do arquivo de log com data de hoje
LOG_FILE = f"data/logs/jarvis_{datetime.now().strftime('%Y-%m-%d')}.log"

# Formato das mensagens de log
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado para o módulo indicado.
    
    Uso:
        from app.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Mensagem de info")
        logger.error("Mensagem de erro")
    
    Os logs são exibidos no terminal E salvos em data/logs/
    """
    logger = logging.getLogger(name)

    # Evita adicionar handlers duplicados
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Handler para o terminal (colorido e legível)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    # Handler para arquivo (guarda tudo, incluindo DEBUG)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
