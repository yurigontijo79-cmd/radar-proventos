"""Camada de banco de dados.

Aqui criamos:
- engine do SQLAlchemy
- sessão de banco
- Base declarativa para os models

Tudo bem básico, limpo e didático, para servir de fundação sem truque.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Fornece uma sessão por requisição.

    Esse padrão evita sair abrindo conexão manual toda hora.
    O FastAPI injeta a dependência e no final a sessão é fechada.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
