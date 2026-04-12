# ============================================================
# tests/test_memory.py
# Testes dos endpoints de memória
# ============================================================

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)


# ── Testes de Memória ────────────────────────────────────────

def test_list_memories_empty():
    """Deve retornar lista vazia quando não há memórias."""
    response = client.get("/memory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_memory():
    """Deve criar uma nova memória com sucesso."""
    payload = {
        "content": "O usuário prefere respostas curtas",
        "memory_type": "preferencia",
        "relevance": 0.9,
    }
    response = client.post("/memory/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == payload["content"]
    assert data["memory_type"] == payload["memory_type"]
    assert "id" in data
    return data["id"]


def test_get_memory():
    """Deve buscar uma memória existente pelo ID."""
    # Cria uma memória primeiro
    create_resp = client.post("/memory/", json={"content": "Memória de teste", "memory_type": "nota"})
    memory_id = create_resp.json()["id"]

    # Busca pelo ID
    response = client.get(f"/memory/{memory_id}")
    assert response.status_code == 200
    assert response.json()["id"] == memory_id


def test_get_nonexistent_memory():
    """Deve retornar 404 para memória inexistente."""
    response = client.get("/memory/99999")
    assert response.status_code == 404


def test_update_memory():
    """Deve atualizar o conteúdo de uma memória."""
    create_resp = client.post("/memory/", json={"content": "Conteúdo original", "memory_type": "fato"})
    memory_id = create_resp.json()["id"]

    update_resp = client.put(f"/memory/{memory_id}", json={"content": "Conteúdo atualizado"})
    assert update_resp.status_code == 200
    assert update_resp.json()["content"] == "Conteúdo atualizado"


def test_delete_memory():
    """Deve deletar uma memória existente."""
    create_resp = client.post("/memory/", json={"content": "Para deletar", "memory_type": "nota"})
    memory_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/memory/{memory_id}")
    assert delete_resp.status_code == 200

    # Confirma que foi deletada
    get_resp = client.get(f"/memory/{memory_id}")
    assert get_resp.status_code == 404
