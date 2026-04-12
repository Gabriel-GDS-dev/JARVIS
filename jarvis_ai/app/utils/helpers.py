# ============================================================
# app/utils/helpers.py
# Funções utilitárias usadas em todo o projeto
# ============================================================

from datetime import datetime


def truncate(text: str, max_length: int = 100) -> str:
    """Trunca um texto longo adicionando '...' no final."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_datetime(dt: datetime) -> str:
    """Formata um datetime para exibição amigável em português."""
    return dt.strftime("%d/%m/%Y às %H:%M")


def sanitize_input(text: str, max_length: int = 5000) -> str:
    """
    Sanitiza a entrada do usuário:
    - Remove espaços extras nas extremidades
    - Limita o tamanho máximo
    """
    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length]
    return text
