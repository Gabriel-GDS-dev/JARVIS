# ============================================================
# app/core/database.py
# Configuração do banco de dados SQLite com SQLAlchemy
# ============================================================

import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Garante que a pasta /data existe antes de criar o banco
os.makedirs("data", exist_ok=True)

# Cria o engine do SQLAlchemy
# connect_args é necessário apenas para SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # necessário para SQLite + FastAPI
    echo=(settings.environment == "development"),  # mostra SQL no terminal em dev
)

# Habilita chaves estrangeiras no SQLite (desativado por padrão)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Fábrica de sessões — use para criar conexões com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para todos os models SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Dependency do FastAPI — fornece uma sessão do banco por requisição.
    
    Uso nos endpoints:
        from app.core.database import get_db
        from sqlalchemy.orm import Session
        from fastapi import Depends
        
        @app.get("/exemplo")
        def minha_rota(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Cria todas as tabelas no banco de dados.
    Chamado uma vez ao iniciar a aplicação.
    """
    # Importa os models para que o SQLAlchemy os registre
    from app.models import chat, memory, user  # noqa: F401
    Base.metadata.create_all(bind=engine)
