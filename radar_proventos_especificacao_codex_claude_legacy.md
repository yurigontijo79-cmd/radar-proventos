# Radar de Proventos — Especificação de Produto + Arquitetura + Algoritmo

## Objetivo
Criar um aplicativo que busque na internet dados oficiais e semioficiais sobre proventos de ações brasileiras (dividendos, JCP e eventos correlatos), normalize essas informações, cruze com a carteira do usuário e apresente tudo de forma simples, visual e útil para tomada de decisão.

O app deve responder, com o menor atrito possível:
- Quem anunciou proventos.
- Qual o valor por ação.
- Qual a data-com.
- Qual a data ex-dividendo.
- Qual a data de pagamento.
- Se ainda dá tempo de comprar.
- Se o usuário já garantiu o direito ao provento.
- Quanto o usuário tende a receber.
- Quais empresas provavelmente anunciarão proventos em breve.

---

## 1. Problema real a ser resolvido
O problema não é apenas “ver dividendos”.

O problema real é consolidar quatro dimensões em uma interface única:
1. O que já foi oficialmente anunciado.
2. O que ainda dá para fazer operacionalmente.
3. O que a carteira do usuário já garantiu.
4. O que provavelmente virá em breve, mesmo antes do anúncio.

Hoje essas informações costumam ficar dispersas entre:
- comunicados de RI,
- documentos da CVM,
- dados da B3,
- sites agregadores,
- e planilhas mentais do investidor.

O aplicativo deve reduzir essa fragmentação.

---

## 2. Premissas do produto

### 2.1 Fonte da verdade
O app deve trabalhar com hierarquia de confiança:

**Fontes primárias / oficiais:**
- CVM / RAD / Empresas.NET
- Relações com Investidores (RI) das empresas
- B3 / Área do Investidor / APIs autorizadas

**Fontes secundárias / apoio:**
- calendários de dividendos e agregadores de mercado
- usados apenas para conferência, enriquecimento ou UX, nunca como fonte suprema em caso de conflito

### 2.2 Separação conceitual obrigatória
O app deve distinguir claramente:
- **Evento oficial**: já anunciado por fonte oficial.
- **Evento provisionado ao investidor**: já reconhecido para a carteira do usuário.
- **Evento estimado**: previsão baseada em histórico e fundamentos.

Eventos estimados devem vir sempre com selo claro:
**ESTIMATIVA — NÃO OFICIAL**

### 2.3 Filosofia de UX
A interface deve privilegiar:
- leitura rápida,
- baixa fricção,
- informação operacional,
- organização temporal.

Não pode virar uma feijoada de dados. O produto deve organizar o tempo do dividendo.

---

## 3. Requisitos funcionais

### 3.1 Cadastro mestre de empresas
O sistema deve manter um universo de companhias listadas com ao menos:
- `company_id`
- `nome_oficial`
- `ticker_principal`
- `setor`
- `codigo_cvm`
- `url_ri`
- `status_ativo`

### 3.2 Coleta de documentos
O sistema deve buscar documentos em múltiplas fontes:
- CVM / RAD
- RI oficial
- B3 / Área do Investidor (mediante autorização do usuário)

### 3.3 Classificação de documentos
Cada documento coletado deve ser classificado quanto à probabilidade de conter informação relevante sobre proventos.

Palavras-chave positivas:
- dividendo
- dividendos
- juros sobre capital próprio
- JCP
- proventos
- remuneração aos acionistas
- aviso aos acionistas
- data-com
- ex-dividendo
- pagamento

Palavras-chave negativas ou neutras:
- recompra
- grupamento
- cisão
- OPA
- AGE
- AGO
- resultado trimestral (pode ser apenas contexto)

### 3.4 Extração de eventos
De documentos classificados como relevantes, o sistema deve extrair:
- empresa
- ticker
- tipo de provento
- valor por ação
- data do anúncio
- data-com
- data ex-dividendo
- data de pagamento
- observações tributárias, quando existirem
- URL da fonte
- título do documento
- nível de confiança

### 3.5 Normalização
Os dados extraídos devem ser convertidos para um formato único, consistente e auditável.

Exemplo de estrutura:

```json
{
  "company": "Banco do Brasil",
  "ticker": "BBAS3",
  "event_type": "JCP",
  "amount_per_share": 0.35,
  "announcement_date": "2026-03-01",
  "record_date": "2026-03-20",
  "ex_date": "2026-03-21",
  "payment_date": "2026-04-15",
  "source_type": "RI",
  "source_url": "https://...",
  "confidence": "official",
  "is_estimated": false
}
```

### 3.6 Deduplicação
O mesmo evento pode aparecer em:
- RI
- CVM
- B3
- republicações
- agregadores

A deduplicação pode usar chave composta como:
- ticker
- tipo de provento
- valor por ação
- data-com
- data de pagamento

Regra de desempate:
1. Fonte oficial mais recente.
2. RI e CVM prevalecem sobre cópias secundárias.
3. Se houver conflito, o evento deve ser marcado para revisão ou exibir sinalização de inconsistência.

### 3.7 Classificação temporal
Cada evento deve receber um status operacional automático.

Regras sugeridas:
- `ainda_da_tempo`: hoje < data-com
- `ultimo_dia`: hoje = data-com
- `pagamento_pendente`: hoje >= data ex e hoje < pagamento
- `pago`: hoje >= pagamento
- `dados_incompletos`: quando datas essenciais faltarem

### 3.8 Cruzamento com carteira do usuário
Se o usuário possuir posição em determinado ticker, o sistema deve calcular:
- quantidade elegível
- valor previsto bruto
- cronograma de recebimento
- eventos já garantidos
- eventos perdidos

Exemplo:
- usuário possui 100 ações de BBAS3
- JCP = R$ 0,35 por ação
- valor bruto previsto = R$ 35,00

### 3.9 Módulo preditivo
O sistema deve estimar proventos futuros antes do anúncio, usando:
- histórico de pagamentos
- regularidade temporal
- payout médio
- payout estável ou instável
- lucro recente
- fluxo de caixa
- política de dividendos
- setor da empresa

Saída esperada:
- ticker
- janela provável de anúncio
- valor estimado por ação
- score de confiança da previsão

---

## 4. Perguntas que o app precisa responder
O app, do ponto de vista de produto, deve responder de forma nativa:

### Mercado
- Quem vai pagar proventos mais próximos?
- Quem ainda está em janela de compra para ter direito?
- Quem já está ex-dividendo, mas ainda vai pagar?
- Qual o valor por ação e quando cai?

### Carteira do usuário
- Quais proventos meus ativos já garantiram?
- Quanto vou receber nos próximos 7, 30 e 90 dias?
- Quais eventos da minha carteira ainda exigem ação antes da data-com?

### Inteligência / previsão
- Quais empresas têm histórico mais previsível?
- Quais devem anunciar em breve?
- Quanto é o dividendo estimado, caso se repita o padrão histórico?

---

## 5. Telas do produto

### 5.1 Tela principal — Radar de Proventos
Lista em cards ou tabela com:
- empresa
- ticker
- tipo de provento
- valor por ação
- data-com
- data ex
- pagamento
- status visual
- selo de confiança

Status visuais sugeridos:
- Ainda dá tempo
- Último dia
- Já fechou
- Pagamento em breve
- Pago
- Estimado

### 5.2 Tela Calendário
Visualização temporal com linha do tempo:
- anúncio
- data-com
- data ex
- pagamento

### 5.3 Tela Previsão
Lista de empresas com maior chance de anunciar em breve:
- ticker
- score
- payout médio
- frequência histórica
- janela provável
- valor estimado

### 5.4 Tela Minha Carteira
Cruzamento da posição do usuário com proventos:
- ticker
- quantidade
- provento por ação
- valor previsto
- data de pagamento
- status

### 5.5 Tela Caixa Futuro
Resumo financeiro visual:
- total previsto em 7 dias
- total previsto em 30 dias
- total previsto em 90 dias
- distribuição por ativo

---

## 6. Alertas úteis
O sistema deve oferecer alertas para:
- novo provento anunciado de ativo da carteira
- faltam 1 ou 2 dias para a data-com
- pagamento amanhã
- pagamento hoje
- empresa entrou em faixa alta de probabilidade de anúncio

---

## 7. Fontes de dados e papel de cada uma

### 7.1 CVM / RAD / Empresas.NET
Uso principal:
- documentos oficiais de companhias abertas
- fatos relevantes
- avisos aos acionistas
- comunicados com proventos

### 7.2 RI das empresas
Uso principal:
- espelho institucional dos documentos mais importantes
- muitas vezes o local mais legível para extração

### 7.3 B3 / Área do Investidor / APIs autorizadas
Uso principal:
- posição do investidor
- eventos provisionados ao investidor
- movimentações e dados personalizados por carteira

### 7.4 Agregadores e sites de calendário
Uso principal:
- apoio visual
- checagem rápida
- experiência de navegação

Nunca devem sobrepor uma divergência de fonte oficial.

---

## 8. Arquitetura recomendada

### 8.1 Visão geral
Arquitetura em quatro camadas:

1. **Coleta**
2. **Normalização e persistência**
3. **Inteligência e regras de negócio**
4. **API e visualização**

### 8.2 Stack sugerida

#### Backend
- Python
- FastAPI
- APScheduler ou Celery para jobs
- PostgreSQL
- Redis para cache e filas leves

#### Coleta
- `httpx` ou `requests`
- `BeautifulSoup` / `lxml`
- `Playwright` apenas quando a fonte exigir renderização JS

#### Extração
- regex para MVP
- parser de datas BR
- parser monetário BR
- NLP opcional em fase posterior

#### Frontend
- React ou Next.js
- tabela filtrável
- cards de eventos
- calendário/linha do tempo
- filtros rápidos por status

#### Infra
- Docker
- deploy em VPS, Railway, Render, Fly ou similar

---

## 9. Modelo de dados

### 9.1 Tabela `companies`
```sql
id
name
ticker
sector
cvm_code
ri_url
active
created_at
updated_at
```

### 9.2 Tabela `source_documents`
```sql
id
company_id
source_type
url
title
published_at
content_hash
raw_text
classification_score
created_at
updated_at
```

### 9.3 Tabela `dividend_events`
```sql
id
company_id
ticker
event_type
amount_per_share
announcement_date
record_date
ex_date
payment_date
currency
source_document_id
confidence
status
is_estimated
created_at
updated_at
```

### 9.4 Tabela `holdings`
```sql
id
user_id
ticker
quantity
avg_price
source
created_at
updated_at
```

### 9.5 Tabela `predicted_events`
```sql
id
company_id
ticker
estimated_amount
expected_window_start
expected_window_end
prediction_score
method_version
created_at
updated_at
```

---

## 10. Algoritmo principal

### 10.1 Pipeline diário
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

### 10.2 Busca de documentos
```python
def fetch_new_documents(company):
    docs = []
    docs += fetch_cvm_documents(company.cvm_code)
    docs += fetch_ri_documents(company.ri_url)
    return deduplicate_docs(docs)
```

### 10.3 Classificação de relevância
```python
def is_dividend_related(doc):
    text = doc.raw_text.lower()
    positive_terms = [
        "dividendo",
        "dividendos",
        "juros sobre capital próprio",
        "jcp",
        "proventos",
        "remuneração aos acionistas",
        "aviso aos acionistas",
        "data-com",
        "ex-dividendo",
        "pagamento"
    ]

    score = sum(1 for term in positive_terms if term in text)
    return score >= 1
```

### 10.4 Extração de campos
```python
def extract_dividend_event(doc):
    text = doc.raw_text

    amount = extract_money(text)
    record_date = extract_date_after_keywords(text, ["data-com", "data com"])
    ex_date = extract_date_after_keywords(text, ["data ex", "ex-dividendo", "ex dividendo"])
    payment_date = extract_date_after_keywords(text, ["pagamento", "será pago em"])
    event_type = detect_event_type(text)

    if not amount and not payment_date:
        return None

    return {
        "amount_per_share": amount,
        "record_date": record_date,
        "ex_date": ex_date,
        "payment_date": payment_date,
        "event_type": event_type,
        "source_title": doc.title,
    }
```

### 10.5 Classificação temporal
```python
def classify_status(today, record_date, ex_date, payment_date):
    if record_date and today < record_date:
        return "ainda_da_tempo"
    if record_date and today == record_date:
        return "ultimo_dia"
    if ex_date and payment_date and ex_date <= today < payment_date:
        return "pagamento_pendente"
    if payment_date and today >= payment_date:
        return "pago"
    return "dados_incompletos"
```

---

## 11. Módulo preditivo

### 11.1 Ideia central
Estimar proventos futuros com base em regularidade histórica e fundamentos públicos.

### 11.2 Fórmula-base conceitual
```python
dividendo_estimado = lucro_por_acao * payout_medio
```

### 11.3 Score de probabilidade
Exemplo de score ponderado:
```python
score = (
    0.35 * regularity_score(history) +
    0.25 * timing_score(history) +
    0.20 * payout_stability_score(history) +
    0.10 * earnings_score(latest_financials) +
    0.10 * cash_score(latest_financials)
)
```

### 11.4 Saída prevista
```json
{
  "ticker": "BBSE3",
  "estimated_amount": 1.20,
  "prediction_score": 0.86,
  "expected_window_start": "2026-04-01",
  "expected_window_end": "2026-05-15",
  "is_estimated": true
}
```

### 11.5 Regras de transparência
Toda previsão deve exibir:
- score
- base histórica usada
- janela provável
- selo de estimativa

---

## 12. Regras de UX e visualização

### 12.1 O que priorizar
- clareza temporal
- separação entre oficial e estimado
- leitura escaneável
- filtros úteis
- pouca fricção

### 12.2 O que evitar
- excesso de campos na mesma tela
- misturar estimado e confirmado sem selo
- interfaces que exijam leitura contábil do usuário
- scraping dependente exclusivamente de sites secundários

### 12.3 Filtros mínimos
- todos
- ainda dá tempo
- pagamento em 7 dias
- pago
- estimado
- minha carteira

---

## 13. Roadmap sugerido

### Fase 1 — MVP forte
- cadastro de empresas
- coleta de CVM e RI
- classificação e extração básica
- tabela de eventos
- status temporal
- carteira manual
- cálculo de caixa futuro

### Fase 2 — Integração com investidor
- importação CSV da carteira
- integração com B3 / APIs autorizadas
- eventos provisionados por investidor
- alertas personalizados

### Fase 3 — Inteligência
- predição de próximos proventos
- ranking de previsibilidade
- comparador entre empresas
- score setorial

---

## 14. Critérios de qualidade do produto
O app será considerado bom se conseguir:

1. Ser confiável o suficiente para uso diário.
2. Mostrar em segundos se ainda dá tempo de comprar.
3. Dizer claramente o que é oficial e o que é estimado.
4. Cruzar proventos com a carteira sem dor de cabeça.
5. Mostrar quando o dinheiro vai cair.
6. Organizar o fluxo temporal dos eventos.

---

## 15. Decisões de produto já tomadas
Com base na auditoria da conversa, as seguintes decisões já estão definidas:

- O app não será apenas um calendário de dividendos.
- O app deve organizar o tempo do provento.
- A informação oficial terá prioridade sobre agregadores.
- A predição é desejada, mas sempre rotulada como estimativa.
- O foco de UX é simplicidade operacional, não excesso de dado bruto.
- O app deve servir tanto para olhar o mercado quanto para olhar a carteira pessoal.

---

## 16. Frase-guia do projeto
**Fonte oficial para verdade. Camada preditiva para oportunidade. Interface simples para não virar feijoada.**

---

## 17. Prompt curto para Codex / Claude
Use este prompt se quiser colar em outro modelo e pedir a implementação:

```text
Construa um MVP de um aplicativo chamado Radar de Proventos.

Objetivo:
- coletar dados oficiais de dividendos/JCP de empresas brasileiras,
- normalizar esses eventos,
- cruzar com a carteira do usuário,
- e exibir tudo de forma simples e operacional.

Fontes prioritárias:
- CVM / RAD / Empresas.NET
- RI das empresas
- B3 / Área do Investidor / APIs autorizadas

Funcionalidades mínimas:
1. Cadastro mestre de empresas listadas.
2. Coleta periódica de documentos oficiais.
3. Classificação de documentos relacionados a proventos.
4. Extração dos campos: ticker, tipo, valor por ação, anúncio, data-com, ex-date e pagamento.
5. Normalização e deduplicação dos eventos.
6. Classificação temporal: ainda dá tempo, último dia, pagamento pendente, pago.
7. Tela principal com radar de proventos.
8. Tela de calendário.
9. Carteira manual do usuário com cálculo de valor previsto a receber.
10. Módulo inicial de previsão com score baseado em payout, histórico e lucro recente.

Stack sugerida:
- FastAPI no backend
- PostgreSQL
- Redis opcional
- Next.js no frontend
- BeautifulSoup/lxml para scraping
- Playwright apenas quando necessário

Entregue:
- arquitetura de pastas,
- schema do banco,
- endpoints principais,
- jobs de coleta,
- funções de parsing,
- protótipo das telas,
- e um plano de implementação por etapas.
```

---

## 18. Prompt expandido para outro modelo implementar tudo

```text
Quero que você implemente um projeto chamado Radar de Proventos.

Descrição do produto:
O Radar de Proventos é um app que coleta e organiza dados de dividendos, JCP e proventos correlatos de ações brasileiras. Ele deve unir em uma interface só:
- o que já foi oficialmente anunciado,
- o que ainda dá tempo de comprar,
- o que a carteira do usuário já garantiu,
- e o que provavelmente será anunciado em breve.

Regras fundamentais:
1. A fonte da verdade deve ser oficial: CVM, RI das empresas e B3.
2. Sites agregadores podem ser usados apenas como apoio.
3. O sistema deve separar claramente eventos oficiais de eventos estimados.
4. O produto deve priorizar simplicidade operacional e leitura rápida.
5. O app deve mostrar o tempo do provento, não apenas uma lista crua de dividendos.

Módulos do sistema:
- companies
- source_documents
- dividend_events
- holdings
- predicted_events

Campos mínimos por evento:
- empresa
- ticker
- tipo de provento
- valor por ação
- data do anúncio
- data-com
- data ex-dividendo
- data de pagamento
- fonte
- confiança
- flag de estimativa

Status temporais:
- ainda_da_tempo
- ultimo_dia
- pagamento_pendente
- pago
- dados_incompletos

Stack sugerida:
- backend em FastAPI
- PostgreSQL
- Redis opcional
- frontend em Next.js
- scraping com requests/httpx + BeautifulSoup/lxml
- Playwright apenas quando necessário
- jobs agendados para coleta

Quero que você produza:
1. arquitetura completa do projeto,
2. schema SQL inicial,
3. modelos ORM,
4. endpoints REST,
5. pipeline diário de coleta,
6. parser de documentos de proventos,
7. lógica de deduplicação,
8. módulo inicial de previsão,
9. frontend com tela principal, calendário, carteira e previsão,
10. instruções para rodar localmente.

Faça em modo pragmático, com foco em MVP forte e expansível.
```
