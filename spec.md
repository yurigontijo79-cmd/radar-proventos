# Radar de Proventos — Especificação Consolidada

## 1. Problema que o produto resolve

O produto deve transformar anúncios dispersos de proventos em uma visão simples, operacional e preditiva.

O usuário quer responder rapidamente:

- quem anunciou dividendos ou JCP;
- qual o valor por ação;
- qual a data-com;
- qual a data ex-dividendo;
- qual a data de pagamento;
- se ainda dá tempo de comprar para ter direito;
- se o usuário já garantiu o provento com base na carteira;
- quais empresas têm maior chance de anunciar em breve, mesmo antes do anúncio oficial.

## 2. Objetivo do MVP

Entregar um aplicativo web com backend e frontend que:

1. colete anúncios de proventos em fontes oficiais;
2. normalize os eventos em um formato único;
3. exiba um radar de proventos futuros e recentes;
4. permita cadastrar a carteira manualmente;
5. calcule o caixa futuro esperado da carteira;
6. ofereça um módulo inicial de previsão com base em histórico.

## 3. Fontes de dados

### 3.1 Fontes primárias
- CVM / RAD / Empresas.NET
- Relações com Investidores (RI) das empresas
- B3 / Área do Investidor / APIs autorizadas quando houver integração do usuário

### 3.2 Fontes secundárias
- Podem ser usadas apenas para conferência visual e comparação
- Não devem ser a fonte da verdade do sistema

## 4. Entidades principais

### Company
- id
- nome oficial
- ticker
- código CVM
- setor
- url do RI
- ativo

### SourceDocument
- id
- company_id
- source_type
- url
- title
- published_at
- raw_text
- content_hash
- classification_score

### DividendEvent
- id
- company_id
- ticker
- event_type (DIVIDEND, JCP, BONUS)
- amount_per_share
- announcement_date
- record_date (data-com)
- ex_date
- payment_date
- currency
- source_document_id
- confidence (official, inferred, estimated)
- status (ainda_da_tempo, ultimo_dia, pagamento_pendente, pago)
- is_estimated

### Holding
- id
- user_id
- ticker
- quantity
- avg_price
- source

### PredictedEvent
- id
- company_id
- ticker
- estimated_amount
- expected_window_start
- expected_window_end
- prediction_score
- method_version

## 5. Regras de negócio

### 5.1 Classificação temporal
- hoje < data-com => ainda_da_tempo
- hoje = data-com => ultimo_dia
- hoje >= ex_date e hoje < payment_date => pagamento_pendente
- hoje >= payment_date => pago

### 5.2 Deduplicação
Considerar mesma chave lógica:
- ticker
- event_type
- amount_per_share
- record_date
- payment_date

Em caso de conflito:
1. fonte oficial mais confiável vence;
2. documento mais recente vence;
3. registrar histórico da mudança.

### 5.3 Cálculo de provento esperado por carteira
valor_previsto = quantidade * valor_por_acao

## 6. Pipeline do sistema

1. carregar universo de empresas;
2. buscar documentos novos em CVM e RI;
3. classificar documentos relacionados a proventos;
4. extrair campos com regex e heurísticas;
5. normalizar datas e valores;
6. deduplicar eventos;
7. classificar status temporal;
8. cruzar com holdings do usuário;
9. calcular caixa futuro;
10. gerar previsões.

## 7. Algoritmo de previsão

### 7.1 Ideia
Estimar proventos antes do anúncio oficial usando:
- histórico de pagamentos;
- payout médio;
- lucro recente por ação;
- sazonalidade;
- consistência temporal;
- solidez de caixa.

### 7.2 Fórmula base
estimativa = lucro_por_acao * payout_medio

### 7.3 Score sugerido
score =
- 0.35 * regularidade_histórica
- 0.25 * proximidade_da_janela_histórica
- 0.20 * estabilidade_do_payout
- 0.10 * crescimento_de_lucro
- 0.10 * solidez_de_caixa

### 7.4 Regra de transparência
Eventos previstos devem aparecer com selo explícito:
- ESTIMATIVA
- NÃO OFICIAL

## 8. Arquitetura técnica

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- Pydantic
- APScheduler ou Celery para jobs
- PostgreSQL
- Redis opcional

### Coleta
- httpx / requests
- BeautifulSoup / lxml
- Playwright apenas quando necessário

### Frontend
- React
- Vite ou Next.js
- componentes simples de tabela, cards e filtros

### Infra
- Docker
- docker-compose para ambiente local

## 9. Telas do MVP

### 9.1 Radar
Exibir tabela com:
- ticker
- empresa
- tipo
- valor
- data-com
- ex
- pagamento
- status

### 9.2 Calendário
Exibir eventos em timeline por data.

### 9.3 Minha carteira
Exibir holdings cadastradas e proventos esperados.

### 9.4 Previsão
Exibir ranking de probabilidade de novos anúncios.

## 10. API sugerida

### Companies
- GET /companies
- POST /companies

### Events
- GET /events
- GET /events/upcoming
- GET /events/predicted
- POST /events/recompute-status

### Holdings
- GET /holdings
- POST /holdings
- DELETE /holdings/{id}

### Dashboard
- GET /dashboard/summary
- GET /dashboard/cashflow

### Jobs
- POST /jobs/run-ingestion
- POST /jobs/run-predictions

## 11. Roadmap

### Fase 1
- cadastro de empresas
- scraper de documentos
- parser de proventos
- radar de proventos
- holdings manuais

### Fase 2
- integração com B3 / Área do Investidor
- projeção automática de caixa por CPF autorizado
- alertas

### Fase 3
- motor preditivo mais robusto
- ranking de previsibilidade por empresa
- notificações e watchlists

## 12. Critérios de qualidade
- sempre priorizar fonte oficial;
- nunca misturar dado oficial e previsto sem etiqueta;
- deixar trilha de auditoria por documento;
- manter interface simples e operacional.
