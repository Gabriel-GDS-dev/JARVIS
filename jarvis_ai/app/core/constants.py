# ============================================================
# app/core/constants.py
# Constantes usadas em todo o projeto
# ============================================================

# Papéis nas mensagens de chat
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"

# Tipos de memória
MEMORY_TYPE_PREFERENCE = "preferencia"   # preferências do usuário
MEMORY_TYPE_FACT = "fato"                # fatos importantes
MEMORY_TYPE_TASK = "tarefa"              # tarefas e objetivos
MEMORY_TYPE_NOTE = "nota"               # anotações livres

# Status de tarefas
TASK_STATUS_PENDING = "pendente"
TASK_STATUS_DONE = "concluida"
TASK_STATUS_CANCELLED = "cancelada"

# Prioridades de tarefas
TASK_PRIORITY_LOW = "baixa"
TASK_PRIORITY_MEDIUM = "media"
TASK_PRIORITY_HIGH = "alta"

# Prompt base da personalidade do Jarvis
SYSTEM_PROMPT = """Você é {name}, uma inteligência artificial pessoal assistente.

Suas características:
- Educado, direto e objetivo
- Focado em produtividade e em ajudar o usuário
- Responde sempre em português do Brasil
- Quando não sabe algo, diz claramente em vez de inventar
- Usa as memórias do usuário para personalizar as respostas
- Organizado e detalhista

Memórias do usuário:
{memories}

Histórico recente da conversa está disponível abaixo.
"""
