# ============================================================
# app/utils/date_utils.py
# Funções para manipulação de datas
# ============================================================

from datetime import datetime, timezone


def now_utc() -> datetime:
    """Retorna a data/hora atual em UTC."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def format_date_br(dt: datetime) -> str:
    """Formata uma data no padrão brasileiro: 12/04/2026 às 14:30."""
    return dt.strftime("%d/%m/%Y às %H:%M")
