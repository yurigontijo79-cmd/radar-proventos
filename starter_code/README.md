# Radar de Proventos — Starter Kit

Este starter kit existe para acelerar a primeira subida do projeto.

## Stack
- Backend: FastAPI
- Banco: PostgreSQL
- Frontend: React + Vite
- Orquestração local: Docker Compose

## Como rodar

### 1. Suba o banco
```bash
docker compose up -d db
```

### 2. Rode o backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Rode o frontend
```bash
cd frontend
npm install
npm run dev
```

## Observação
Os scrapers estão estruturados para começar com mocks e adaptadores simples.
Isso permite construir o fluxo sem travar logo de cara em autenticação, anti-bot ou páginas complexas.
