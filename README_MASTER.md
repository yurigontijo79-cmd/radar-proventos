# Radar de Proventos — README Mestre de Produção

## 1. Visão do produto

Radar de Proventos é um aplicativo para coletar, normalizar, classificar e visualizar eventos de proventos de ações brasileiras, com foco em dividendos e JCP. O sistema combina fontes oficiais, agenda operacional e uma camada preditiva para transformar disclosures dispersos em informação acionável.

### Problema que resolve
Hoje os dados de proventos estão espalhados entre RI das empresas, CVM, B3 e plataformas secundárias. O investidor precisa montar mentalmente a linha do tempo:
- anúncio
- data-com
- data ex-dividendo
- data de pagamento
- elegibilidade da própria carteira

O Radar de Proventos centraliza isso e responde, em linguagem operacional:
- quem anunciou proventos
- quem vai pagar em breve
- em quais ativos ainda dá tempo de entrar
- quais pagamentos o usuário já garantiu
- quais empresas provavelmente anunciarão em breve

---

## 2. Objetivos do MVP

### Objetivo principal
Entregar um painel funcional com coleta oficial/semi-oficial de eventos, banco persistente, API e interface web simples.

### Objetivos específicos
1. Coletar eventos de proventos em fontes oficiais.
2. Extrair campos estruturados dos documentos.
3. Normalizar e deduplicar eventos.
4. Classificar status temporal dos eventos.
5. Permitir cadastro/importação manual de carteira.
6. Cruzar eventos com a carteira do usuário.
7. Exibir dashboard de próximos proventos e caixa previsto.
8. Exibir estimativas de próximos anúncios com score separado de dados oficiais.

---

## 3. Escopo por fase

### Fase 1 — MVP operacional
- cadastro de empresas/tickers
- scraper CVM / RI
- parser de proventos
- banco PostgreSQL
- API FastAPI
- frontend React/Next básico
- filtros por status
- carteira manual
- projeção de caixa do usuário

### Fase 2 — Robustez
- scheduler e filas
- logs e auditoria
- revisão manual de parsing
- autenticação
- importação CSV de carteira
- testes automatizados
- alertas básicos

### Fase 3 — Inteligência
- predição de próximos proventos
- score de confiança
- ranking de previsibilidade
- alertas inteligentes
- comparação entre empresas/setores

### Fora do escopo inicial
- IR completo
- login bancário direto
- day trade
- multi-mercado
- app mobile nativo

---

## 4. Requisitos funcionais

### RF-01 — Cadastro mestre de empresas
O sistema deve manter uma base de empresas com:
- nome oficial
- ticker
- setor
- código CVM
- URL de RI
- status ativo/inativo

### RF-02 — Coleta de documentos
O sistema deve buscar periodicamente documentos novos em:
- CVM/RAD/ENET
- RI das empresas

### RF-03 — Classificação de documentos
O sistema deve classificar documentos com potencial de conter proventos usando heurísticas por palavras-chave.

### RF-04 — Extração estruturada
O sistema deve extrair, quando disponíveis:
- ticker
- empresa
- tipo de provento
- valor por ação
- data do anúncio
- data-com
- data ex
- data de pagamento
- observações
- fonte

### RF-05 — Normalização
O sistema deve converter os dados extraídos para um formato único e consistente.

### RF-06 — Deduplicação
O sistema deve evitar eventos duplicados oriundos de múltiplas fontes.

### RF-07 — Classificação temporal
O sistema deve marcar eventos como:
- ainda dá tempo
- último dia
- pagamento pendente
- pago
- indefinido

### RF-08 — Carteira do usuário
O sistema deve permitir:
- cadastro manual de posições
- importação CSV em fase seguinte

### RF-09 — Projeção de caixa
O sistema deve calcular o valor previsto de proventos por ativo e total da carteira.

### RF-10 — Visualização
O sistema deve exibir:
- próximos proventos
- eventos por status
- caixa previsto
- histórico básico
- estimados com selo de não oficial

### RF-11 — Predição
O sistema deve estimar próximos proventos com base em histórico, payout, lucro recente e regularidade, sempre separados dos eventos oficiais.

---

## 5. Requisitos não funcionais

### RNF-01 — Rastreabilidade
Todo evento deve manter referência de origem.

### RNF-02 — Separação entre oficial e estimado
Dados estimados nunca podem ser misturados visualmente com dados oficiais sem marcação clara.

### RNF-03 — Auditabilidade
Toda execução de scraping/parsing deve gerar logs.

### RNF-04 — Idempotência
Rodar o pipeline mais de uma vez não pode multiplicar registros indevidamente.

### RNF-05 — Resiliência
Falha em uma fonte não deve derrubar o pipeline inteiro.

### RNF-06 — Performance razoável
O dashboard deve abrir rapidamente para bases pequenas e médias.

---

## 6. Arquitetura proposta

## Stack
- Backend: Python + FastAPI
- Banco: PostgreSQL
- Cache/Fila: Redis (fase 2)
- Frontend: React ou Next.js
- Agendamento: APScheduler no MVP; Celery depois
- Containers: Docker + docker-compose

## Módulos
1. `company_registry`
2. `source_adapters`
3. `document_classifier`
4. `event_parser`
5. `event_normalizer`
6. `event_repository`
7. `portfolio_module`
8. `prediction_engine`
9. `api_layer`
10. `frontend_dashboard`

## Fluxo
```text
Fonte oficial/RI
→ scraping/coleta
→ classificação
→ parsing
→ normalização
→ deduplicação
→ persistência
→ API
→ dashboard
```

---

## 7. Modelo de dados

### Tabela: companies
- id
- name
- ticker
- cvm_code
- sector
- ri_url
- active
- created_at
- updated_at

### Tabela: source_documents
- id
- company_id
- source_type
- url
- title
- published_at
- content_hash
- raw_text
- classification_score
- processed_at
- created_at

### Tabela: dividend_events
- id
- company_id
- ticker
- event_type
- amount_per_share
- announcement_date
- record_date
- ex_date
- payment_date
- currency
- source_document_id
- confidence
- status
- is_estimated
- notes
- created_at
- updated_at

### Tabela: user_holdings
- id
- user_id
- ticker
- quantity
- avg_price
- source
- created_at
- updated_at

### Tabela: predicted_events
- id
- company_id
- ticker
- estimated_amount
- expected_window_start
- expected_window_end
- prediction_score
- method_version
- notes
- created_at

---

## 8. Endpoints da API

### Health
- `GET /health`

### Companies
- `GET /companies`
- `POST /companies`
- `GET /companies/{ticker}`

### Events
- `GET /events`
- filtros: `ticker`, `status`, `event_type`, `days_ahead`, `official_only`
- `GET /events/{event_id}`

### Predictions
- `GET /predictions`
- `GET /predictions/{ticker}`

### Portfolio
- `GET /portfolio`
- `POST /portfolio`
- `PUT /portfolio/{holding_id}`
- `DELETE /portfolio/{holding_id}`
- `GET /portfolio/cashflow`

### Pipelines/admin
- `POST /admin/pipeline/run`
- `POST /admin/pipeline/recompute-status`
- `POST /admin/pipeline/recompute-predictions`

### Dashboard
- `GET /dashboard/summary`
- `GET /dashboard/upcoming`
- `GET /dashboard/opportunities`

---

## 9. Regras de negócio centrais

### RB-01 — Prioridade de fontes
Quando houver conflito:
1. CVM / documento oficial
2. RI oficial da empresa
3. fonte secundária

### RB-02 — Chave de deduplicação
Usar combinação aproximada:
- ticker
- tipo de provento
- valor por ação
- data-com
- data de pagamento

### RB-03 — Regras de status
- hoje < data-com → `ainda_da_tempo`
- hoje = data-com → `ultimo_dia`
- ex_date <= hoje < payment_date → `pagamento_pendente`
- hoje >= payment_date → `pago`
- caso contrário → `indefinido`

### RB-04 — Predição separada
Predições devem sempre ser salvas em tabela própria e renderizadas com selo visual distinto.

---

## 10. Algoritmo operacional

### Pipeline diário
```python
def daily_pipeline():
    companies = load_companies()

    for company in companies:
        docs = fetch_new_documents(company)

        for doc in docs:
            if not is_dividend_related(doc):
                continue

            event = extract_dividend_event(doc)
            if not event:
                continue

            normalized = normalize_event(event, company)
            upsert_event(normalized)

    recompute_statuses()
    recompute_predictions()
    recompute_user_expected_cashflows()
```

### Classificador inicial
- palavras positivas:
  - dividendo
  - juros sobre capital próprio
  - JCP
  - proventos
  - remuneração aos acionistas
  - aviso aos acionistas

### Parsing inicial
Usar regex e heurísticas para:
- valores monetários em BRL
- datas no padrão brasileiro
- expressões “data-com”, “ex-dividendo”, “pagamento”

### Predição inicial
Fórmula conceitual:
```text
dividendo_estimado = lucro_por_ação × payout_médio
```

Score sugerido:
```text
0.35 * regularidade_histórica +
0.25 * proximidade_da_janela_histórica +
0.20 * estabilidade_do_payout +
0.10 * lucro_recente +
0.10 * caixa/solidez
```

---

## 11. UX do dashboard

### Tela 1 — Radar
Tabela principal com:
- ticker
- empresa
- tipo
- valor
- data-com
- ex
- pagamento
- status

### Tela 2 — Caixa futuro
Cards com:
- próximos 7 dias
- próximos 30 dias
- total previsto por carteira

### Tela 3 — Estimados
Lista separada com:
- ticker
- valor estimado
- janela provável
- score
- aviso de “estimativa, não oficial”

### Tela 4 — Minha carteira
- posições
- proventos previstos por posição
- histórico básico por ativo

### Filtros prioritários
- ainda dá tempo
- pagamento em 7 dias
- oficiais apenas
- estimados
- por ticker

---

## 12. Backlog MVP priorizado

### Bloco 1 — Fundação
1. criar estrutura do repositório
2. subir docker-compose com postgres
3. criar FastAPI básica
4. criar models SQLAlchemy
5. criar migrations

### Bloco 2 — Empresas e eventos
6. CRUD de companies
7. CRUD/listagem de events
8. endpoint de summary

### Bloco 3 — Coleta
9. adapter CVM stub
10. adapter RI stub
11. classificador de documentos
12. parser inicial de proventos
13. normalização
14. deduplicação

### Bloco 4 — Carteira
15. CRUD de holdings
16. cálculo de caixa futuro
17. endpoint `/portfolio/cashflow`

### Bloco 5 — Frontend
18. dashboard inicial
19. tabela de eventos
20. cards de resumo
21. tela de carteira

### Bloco 6 — Predição
22. histórico por ticker
23. score inicial
24. endpoint de predictions
25. tela de estimados

---

## 13. Ordem exata de implementação

```text
1. backend sobe
2. banco sobe
3. models e migrations
4. CRUD companies
5. CRUD events
6. dashboard summary
7. holdings
8. cashflow
9. scraper stubs
10. parser real
11. pipeline agendado
12. predictions
13. frontend refinado
```

---

## 14. Critérios de aceite do MVP

O MVP é considerado aceito se:
1. subir via Docker localmente
2. permitir cadastrar empresas
3. permitir inserir/ler eventos
4. permitir cadastrar carteira
5. calcular caixa futuro da carteira
6. exibir dashboard funcional
7. executar pipeline de coleta/parsing sem quebrar a aplicação
8. separar claramente eventos oficiais de estimados

---

## 15. Riscos e mitigação

### Risco: páginas mudam estrutura
Mitigação: adaptar scraping por adapter isolado.

### Risco: parsing ambíguo
Mitigação: confidence score + revisão manual posterior.

### Risco: duplicidade
Mitigação: hash de documento + chave de evento.

### Risco: mistura entre oficial e previsão
Mitigação: tabelas separadas + badges fortes.

---

## 16. Prompt mestre para IA de implementação

```text
Você vai implementar o projeto Radar de Proventos.

Objetivo:
Construir um MVP funcional que colete, normalize e exiba eventos de dividendos/JCP de ações brasileiras.

Stack obrigatória:
- backend em Python com FastAPI
- banco PostgreSQL
- frontend em React ou Next.js
- docker-compose para ambiente local

Regras:
- separar rigorosamente eventos oficiais e eventos estimados
- manter código modular
- usar boas práticas de tipagem e comentários claros
- criar estrutura pronta para expansão

Entregas mínimas:
- models
- migrations
- endpoints REST
- dashboard básico
- cálculo de caixa futuro
- parser inicial de proventos
- prediction stub
```

---

## 17. Decisão final de produto

Este projeto não é apenas um agregador de dividendos. Ele é um organizador do tempo do provento.

### Fórmula do produto
```text
fonte oficial para verdade
+
camada preditiva para oportunidade
+
interface simples para decisão rápida
```

