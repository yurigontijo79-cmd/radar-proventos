# Radar de Proventos — Starter Kit

Este starter kit entrega um MVP funcional com:
- backend FastAPI;
- frontend React + Vite;
- PostgreSQL;
- docker-compose para subir tudo localmente.

## Stack
- Backend: FastAPI + SQLAlchemy
- Banco: PostgreSQL 16
- Frontend: React 18 + Vite
- Orquestração local: Docker Compose

## Como rodar (modo recomendado)

```bash
cd starter_code
docker compose up --build
```

Serviços:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Docs da API: http://localhost:8000/docs
- Banco: localhost:5432

## Como rodar sem Docker

### 1) Banco
```bash
cd starter_code
docker compose up -d db
```

### 2) Backend
```bash
cd starter_code/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3) Frontend
```bash
cd starter_code/frontend
npm install
npm run dev
```

## Endpoints do MVP implementados

### Companies
- `GET /companies`
- `POST /companies`

### Events
- `GET /events`
- `GET /events/upcoming`
- `GET /events/predicted`
- `POST /events/recompute-status`

### Holdings
- `GET /holdings`
- `POST /holdings`
- `DELETE /holdings/{id}`

### Dashboard
- `GET /dashboard/summary`
- `GET /dashboard/cashflow`

### Jobs
- `POST /jobs/run-ingestion`
- `POST /jobs/run-predictions`

## Observação
Scrapers continuam em modo inicial (adapters/mocks) para validar o pipeline ponta a ponta antes de evoluir coleta oficial.
