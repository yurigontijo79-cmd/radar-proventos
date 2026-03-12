# Prompt de geração para Codex / Claude

Leia `spec.md` e gere um projeto completo chamado `radar-proventos`.

## Objetivo
Criar um aplicativo web para coletar, normalizar, visualizar e prever anúncios de proventos (dividendos e JCP) de empresas brasileiras listadas em bolsa.

## Requisitos obrigatórios
- backend em Python com FastAPI;
- banco PostgreSQL;
- SQLAlchemy 2.x;
- Pydantic para schemas;
- jobs agendáveis para coleta e previsão;
- frontend em React;
- docker-compose funcional;
- comentários didáticos no código, explicando as partes importantes;
- estrutura clara de pastas;
- endpoints REST básicos;
- interface inicial com tabela de eventos, resumo e holdings;
- parser inicial com regex e heurísticas;
- dados previstos claramente marcados como estimativa.

## Escopo do MVP
1. cadastro de empresas;
2. scraper de documentos de RI/CVM simulável ou com adaptadores;
3. parser de documentos para extração de proventos;
4. persistência dos eventos;
5. cálculo de status temporal;
6. holdings manuais;
7. cálculo de caixa futuro esperado;
8. ranking básico de previsões.

## Regras de implementação
- gere código executável, não apenas pseudocódigo;
- inclua arquivo `.env.example`;
- inclua instruções claras de execução no README;
- inclua exemplos de payload para endpoints;
- mantenha o frontend simples, limpo e fácil de evoluir;
- não dependa de serviços pagos;
- prefira bibliotecas maduras e leves;
- se alguma integração oficial exigir credenciais, crie adaptadores e mocks bem separados.

## Entregáveis esperados
- README.md
- backend completo
- frontend completo
- docker-compose.yml
- scripts iniciais de banco
- exemplo de dados seed
- testes básicos pelo menos para parser e regra de status

## Saída desejada
Retorne a árvore do projeto e depois o conteúdo dos arquivos principais.
