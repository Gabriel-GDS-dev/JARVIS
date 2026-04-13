# ============================================================
# app/main.py
# Ponto de entrada da aplicação FastAPI
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.api import routes_chat, routes_memory, routes_health
from app.utils.logger import get_logger

logger = get_logger(__name__)

# ── Cria a instância do FastAPI ──────────────────────────────
app = FastAPI(
    title=f"{settings.jarvis_name} AI",
    description="API da IA Pessoal tipo Jarvis — backend local com Ollama",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI disponível em http://localhost:8000/docs
    redoc_url="/redoc",      # ReDoc disponível em http://localhost:8000/redoc
)

# ── CORS — permite que a interface web acesse a API ──────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Em produção, restrinja para origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Registra as rotas ────────────────────────────────────────
app.include_router(routes_health.router)
app.include_router(routes_chat.router)
app.include_router(routes_memory.router)


# ── Evento de startup ────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    """
    Executado UMA VEZ quando o servidor inicia.
    Cria as tabelas do banco se ainda não existirem.
    """
    logger.info(f"🚀 Iniciando {settings.jarvis_name} AI...")
    create_tables()
    logger.info("✅ Banco de dados pronto.")
    logger.info(f"📖 Documentação: http://localhost:{settings.api_port}/docs")
    logger.info(f"🤖 Modelo: {settings.ollama_model} via {settings.ollama_base_url}")


# ── Rota raiz ────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": f"Bem-vindo ao {settings.jarvis_name} AI!",
        "docs": f"http://localhost:{settings.api_port}/docs",
        "health": f"http://localhost:{settings.api_port}/health",
        "status": f"http://localhost:{settings.api_port}/status",
    }
