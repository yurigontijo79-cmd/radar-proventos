# Radar de Proventos — Starter Kit

Este starter kit entrega um MVP funcional com:
- backend FastAPI;
- frontend React + Vite;
- PostgreSQL;
- docker-compose para subir tudo localmente;
- trilha inicial de coleta real em páginas de RI (beta).

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

## Endpoints disponíveis

### Health
- `GET /health`
- `GET /`

### Companies
- `GET /companies`
- `POST /companies`
  - retorna `201` quando cria
  - retorna `409` quando `ticker` já existe
  - aceita `?idempotent=true` para retornar a empresa existente com `200`

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
- `POST /jobs/run-ingestion` (executa coleta RI beta e persiste documentos/eventos oficiais)
- `POST /jobs/run-predictions` (stub)

## Coleta RI beta (o que realmente faz)
1. Lê empresas ativas com `ri_url` cadastrado.
2. Acessa a página de RI e identifica links com palavras-chave (dividendos/JCP/proventos).
3. Baixa o conteúdo textual dos links candidatos.
4. Salva documento bruto em:
   - tabela `source_documents`;
   - arquivo local `backend/data/raw_documents/*.txt`.
5. Classifica documentos por score heurístico de termos.
6. Extrai evento com parser regex inicial.
7. Persiste apenas eventos **oficiais** (`confidence="official"`, `is_estimated=false`) em `dividend_events`.

## Limitações atuais
- Coleta RI não cobre PDF/JS dinâmico de forma robusta.
- Extração ainda é heurística por regex (sujeita a falso positivo/negativo).
- `run-predictions` continua stub.
- Adaptador CVM continua sem implementação.

## Documentação metodológica
- `backend/docs/INGESTION_METHOD.md`
