# Radar de Proventos — Plano de Implementação Jackado

## Parte 1 — Infra e base
- criar repositório
- docker-compose com postgres
- backend FastAPI rodando
- frontend React/Next rodando
- variáveis de ambiente

## Parte 2 — Modelo de dados
- companies
- source_documents
- dividend_events
- user_holdings
- predicted_events
- migrations Alembic

## Parte 3 — API mínima
- health
- companies CRUD
- events list/detail
- portfolio CRUD
- cashflow
- dashboard summary

## Parte 4 — Pipeline inicial
- company loader
- CVM adapter stub
- RI adapter stub
- classificador por palavras-chave
- parser regex de datas e valores
- normalizador
- deduplicador

## Parte 5 — Dashboard
- cards resumo
- tabela de eventos
- filtros por status
- carteira do usuário
- caixa futuro

## Parte 6 — Predição
- cálculo de payout médio
- estimativa por ticker
- score inicial
- tela separada de estimados

## Parte 7 — Robustez
- logs
- retries
- testes unitários
- testes de integração
- revisão manual futura

## Prioridade absoluta
1. subir ambiente
2. persistir dados
3. exibir dados
4. automatizar coleta
5. adicionar inteligência
