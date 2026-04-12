# ============================================================
# app/schemas/tool_schema.py
# Schemas para o sistema de ferramentas (futuro)
# ============================================================

from typing import Optional, Any, Dict
from pydantic import BaseModel


class ToolRequest(BaseModel):
    """Requisição para executar uma ferramenta."""
    tool_name: str
    parameters: Optional[Dict[str, Any]] = {}


class ToolResponse(BaseModel):
    """Resposta de uma ferramenta."""
    tool_name: str
    result: Any
    success: bool
    error: Optional[str] = None
