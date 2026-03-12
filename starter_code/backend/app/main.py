"""Ponto de entrada da API.

Aqui a aplicação nasce, sobe as tabelas e registra as rotas.
É o centro nervoso do backend.
"""

from fastapi import FastAPI

from app.api.companies import router as companies_router
from app.api.dashboard import router as dashboard_router
from app.api.events import router as events_router
from app.api.holdings import router as holdings_router
from app.api.jobs import router as jobs_router
from app.core.config import settings
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(companies_router)
app.include_router(events_router)
app.include_router(holdings_router)
app.include_router(dashboard_router)
app.include_router(jobs_router)


@app.get("/")
def healthcheck():
    return {"app": settings.app_name, "status": "ok"}
