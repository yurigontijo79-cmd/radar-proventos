# Estrutura sugerida do repositório

```text
radar-proventos/
├─ README.md
├─ .env.example
├─ docker-compose.yml
├─ backend/
│  ├─ requirements.txt
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  └─ database.py
│  │  ├─ api/
│  │  │  ├─ companies.py
│  │  │  ├─ events.py
│  │  │  ├─ holdings.py
│  │  │  ├─ dashboard.py
│  │  │  └─ jobs.py
│  │  ├─ models/
│  │  │  ├─ company.py
│  │  │  ├─ source_document.py
│  │  │  ├─ dividend_event.py
│  │  │  ├─ holding.py
│  │  │  └─ predicted_event.py
│  │  ├─ schemas/
│  │  │  ├─ company.py
│  │  │  ├─ dividend_event.py
│  │  │  ├─ holding.py
│  │  │  └─ dashboard.py
│  │  └─ services/
│  │     ├─ ingestion.py
│  │     ├─ parser.py
│  │     ├─ prediction.py
│  │     └─ status_classifier.py
│  └─ tests/
│     ├─ test_parser.py
│     └─ test_status.py
├─ frontend/
│  ├─ package.json
│  ├─ src/
│  │  ├─ main.jsx
│  │  ├─ App.jsx
│  │  ├─ services/api.js
│  │  ├─ pages/
│  │  │  └─ Dashboard.jsx
│  │  └─ components/
│  │     ├─ SummaryCards.jsx
│  │     ├─ EventsTable.jsx
│  │     └─ HoldingsTable.jsx
├─ database/
│  ├─ init.sql
│  └─ seed.sql
└─ scrapers/
   ├─ cvm_adapter.py
   ├─ ri_adapter.py
   └─ mocks/
```
