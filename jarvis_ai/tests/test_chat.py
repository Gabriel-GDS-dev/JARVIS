# ============================================================
# tests/test_chat.py
# Testes dos endpoints de chat
# ============================================================

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Banco de dados em memória exclusivo para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Substitui o banco real pelo banco de teste."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Sobrescreve a dependency do banco durante os testes
app.dependency_overrides[get_db] = override_get_db

# Cria as tabelas no banco de teste
Base.metadata.create_all(bind=engine)

# Cliente HTTP para os testes
client = TestClient(app)


# ── Testes de Health ─────────────────────────────────────────

def test_health_endpoint():
    """O endpoint /health deve retornar status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_status_endpoint():
    """O endpoint /status deve retornar informações do sistema."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "api" in data
    assert "ollama" in data
    assert "model" in data


def test_root_endpoint():
    """A rota raiz deve retornar mensagem de boas-vindas."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# ── Testes de Chat ───────────────────────────────────────────

def test_list_conversations_empty():
    """Deve retornar lista vazia quando não há conversas."""
    response = client.get("/chat/conversations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_conversation():
    """Deve retornar 404 para conversa inexistente."""
    response = client.get("/chat/conversations/99999/messages")
    assert response.status_code == 404


def test_delete_nonexistent_conversation():
    """Deve retornar 404 ao deletar conversa inexistente."""
    response = client.delete("/chat/conversations/99999")
    assert response.status_code == 404
