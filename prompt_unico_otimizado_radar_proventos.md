# PROMPT ÚNICO OTIMIZADO — RADAR DE PROVENTOS
## Versão para Claude / Codex / Cursor / outras IAs de código

Use este prompt depois de subir os arquivos de especificação do projeto.

---

## PROMPT PRINCIPAL

```text
Leia cuidadosamente os arquivos enviados, especialmente:

- README_MASTER.md
- IMPLEMENTATION_PLAN.md
- spec.md
- build_prompt.md
- repo_structure.md
- starter_code/

Sua tarefa é gerar o projeto completo chamado "radar-proventos" como um aplicativo web local, funcional e executável, pronto para rodar com Docker Compose.

# Objetivo do produto
Construir um sistema que:
- colete eventos de proventos/dividendos/JCP em fontes oficiais
- classifique documentos relevantes
- extraia e normalize eventos
- armazene os dados em PostgreSQL
- exponha endpoints via FastAPI
- apresente um dashboard React no navegador
- prepare o terreno para cruzamento com carteira do usuário e motor preditivo

# Stack obrigatória
- Backend: Python + FastAPI
- Banco: PostgreSQL
- Frontend: React
- Infra local: Docker Compose
- Cache/fila: Redis, se necessário
- Scraping/coleta: httpx/requests + BeautifulSoup; Playwright só quando for realmente necessário

# Regras de arquitetura
- arquitetura modular
- separação entre adapters, parsers, services, api, models e prediction
- separar claramente dado bruto e dado tratado
- separar claramente eventos oficiais de eventos estimados
- manter o starter_code como base, expandindo e corrigindo onde necessário
- priorizar código executável em vez de texto explicativo
- não entregar pseudocódigo como saída principal
- não concentrar tudo em um único arquivo
- gerar um repositório coerente, com nomes consistentes e integração real entre camadas

# Escopo mínimo obrigatório do MVP
1. Backend FastAPI funcional
2. PostgreSQL configurado
3. Docker Compose funcional
4. Estrutura de empresas/tickers
5. Coletor inicial de fontes oficiais (CVM / RI)
6. Classificador de documentos relacionados a dividendos/JCP
7. Extractor / parser / normalizer de eventos
8. Persistência dos eventos no banco
9. Endpoints da API para:
   - próximos eventos
   - eventos acionáveis
   - pagamento em breve
   - eventos estimados
   - healthcheck
10. Frontend React com telas:
   - Radar de Proventos
   - Calendário / lista temporal
   - Estimativas
   - Health/status simples
11. README final com instruções reais de execução

# Estrutura esperada do repositório
A estrutura deve seguir a intenção de repo_structure.md, produzindo algo equivalente a:

radar-proventos/
├─ backend/
├─ frontend/
├─ database/
├─ docker-compose.yml
├─ README.md
└─ .env.example

# Modelo de domínio esperado
Cada evento de provento deve ter, sempre que disponível:
- empresa
- ticker
- tipo de provento
- valor por ação
- data do anúncio
- data-com / record date
- data ex
- data de pagamento
- fonte
- status temporal
- confiança (official / estimated)

# Regras de negócio importantes
- "ainda dá tempo" quando a data-com ainda não passou
- "último dia" quando hoje for a data-com
- "pagamento pendente" quando a data ex já passou, mas o pagamento ainda não aconteceu
- "pago" quando a data de pagamento já tiver passado
- previsões devem aparecer sempre marcadas como ESTIMATIVA

# Implementação esperada
Quero código real, com:
- models
- schemas
- services
- adapters
- parser/classifier/normalizer
- rotas da API
- componentes/pages/hooks/services no frontend
- docker-compose funcional
- arquivos de dependências
- README executável

# Entrega
Entregue o projeto completo em blocos organizados por arquivo, respeitando a estrutura do repositório.
Comece pela árvore final de pastas e depois implemente os arquivos.
Se perceber inconsistências nos arquivos enviados, corrija durante a implementação e documente as correções no README final.
```

---

## INSTRUÇÃO DE USO

Depois de colar esse prompt, se a IA vier muito explicativa e pouco prática, responda com:

```text
Quero implementação real agora.
Pare de explicar e entregue o repositório com arquivos completos.
Comece pela árvore final de pastas e depois preencha todos os arquivos do MVP.
```

---

## COMANDO DE CORREÇÃO, SE A RESPOSTA VIER FRACA

```text
A resposta veio incompleta.

Corrija agora com foco em execução real:
- código implementado
- backend funcional
- frontend funcional
- banco configurado
- docker-compose funcional
- README real de execução

Não entregue só descrição.
Não entregue só estrutura.
Entregue arquivos completos e coerentes.
```

---

## COMANDO DE CONTINUAÇÃO, SE PARAR NO MEIO

```text
Continue a partir do ponto atual sem reiniciar o projeto.
Complete os arquivos faltantes e finalize o MVP funcional.
```

---

## COMANDO DE AUDITORIA FINAL

```text
Agora faça uma auditoria completa no repositório gerado.

Verifique:
- imports quebrados
- dependências ausentes
- arquivos citados e não implementados
- rotas não ligadas
- frontend não conectado à API
- variáveis de ambiente faltando
- docker-compose inválido
- inconsistências de nomenclatura

Depois corrija tudo e entregue a versão final consolidada.
```
