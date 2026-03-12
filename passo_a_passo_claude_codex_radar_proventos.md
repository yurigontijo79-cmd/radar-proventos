# PASSO A PASSO — COMO SUBIR O PROJETO “RADAR DE PROVENTOS” NO CLAUDE / CODEX

Este documento foi feito para uso operacional.
Objetivo: pegar o material já pronto do projeto, subir na IA de código e obter um repositório funcional sem quebrar o ritmo.

---

## 1. O que você vai subir

Use o pacote mais completo:

- `README_MASTER.md`
- `IMPLEMENTATION_PLAN.md`
- `spec.md`
- `build_prompt.md`
- `repo_structure.md`
- `starter_code/`

Se quiser simplificar, suba pelo menos:

- `README_MASTER.md`
- `IMPLEMENTATION_PLAN.md`
- `starter_code/`

---

## 2. O que esse material deve gerar

A IA deve gerar um projeto web, não um executável desktop.

Estrutura esperada:

```text
radar-proventos/
├─ backend/
├─ frontend/
├─ database/
├─ docker-compose.yml
├─ README.md
└─ .env.example
```

Resultado esperado:

- backend em FastAPI
- banco PostgreSQL
- frontend React
- docker-compose para subir tudo
- coletores para CVM / RI
- parser de dividendos
- dashboard no navegador

---

## 3. Como usar no CLAUDE ou CODEX

### Método recomendado
Não peça tudo de forma genérica.
Dê uma ordem clara, em etapas.

### Ordem certa
1. fazer leitura do material
2. montar a estrutura do repositório
3. implementar backend base
4. implementar banco
5. implementar scrapers
6. implementar parser
7. implementar API
8. implementar frontend
9. ajustar docker-compose
10. validar execução local

---

## 4. Prompt mestre para a primeira mensagem

Cole isto:

```text
Leia cuidadosamente os arquivos README_MASTER.md, IMPLEMENTATION_PLAN.md, spec.md, build_prompt.md e repo_structure.md.

Objetivo:
Gerar o projeto completo "radar-proventos" como um aplicativo web local, pronto para rodar com Docker.

Stack obrigatória:
- Backend: Python + FastAPI
- Banco: PostgreSQL
- Frontend: React
- Infra local: Docker Compose
- Cache/fila: Redis se necessário

Funções obrigatórias do MVP:
- cadastro/base de empresas
- coleta de documentos de proventos em fontes oficiais (CVM / RI)
- classificação de documentos relacionados a dividendos/JCP
- extração e normalização de eventos
- armazenamento em banco
- endpoints de API
- dashboard web com:
  - próximos eventos
  - ainda dá tempo
  - pagamento em breve
  - eventos estimados
- estrutura preparada para carteira do usuário e motor preditivo

Regras importantes:
- use starter_code como base, expandindo e corrigindo o que for necessário
- mantenha arquitetura modular
- separe dado bruto e dado tratado
- diferencie claramente evento oficial de evento estimado
- gere um repositório completo, coerente e executável

Resultado esperado:
- árvore de pastas final
- arquivos implementados
- docker-compose funcional
- README com instruções de execução
- projeto pronto para abrir no navegador local
```

---

## 5. O que você deve pedir na segunda mensagem

Depois que ele responder com a estrutura, mande:

```text
Agora implemente de fato o backend e o banco.

Entregue:
- models
- schemas
- migrations ou SQL inicial
- serviços
- adapters
- parser/classifier/normalizer
- endpoints do MVP
- docker-compose ajustado

Quero código real, não pseudocódigo.
```

---

## 6. O que pedir na terceira mensagem

```text
Agora implemente o frontend React do MVP.

Telas obrigatórias:
- Radar de proventos
- Calendário
- Eventos estimados
- Health/status simples

A interface deve consumir a API local e abrir no navegador.
Quero componentes, serviços de API, páginas e instruções de execução.
```

---

## 7. O que pedir na quarta mensagem

```text
Agora revise o repositório inteiro e faça uma auditoria de consistência.

Verifique:
- imports quebrados
- nomes inconsistentes
- variáveis de ambiente faltando
- endpoints não conectados ao frontend
- serviços citados e não implementados
- docker-compose inválido
- dependências ausentes

Depois entregue a versão final corrigida.
```

---

## 8. O que pedir na quinta mensagem

```text
Agora gere um README final de produção contendo:

- visão geral
- arquitetura
- estrutura de pastas
- variáveis de ambiente
- como subir localmente
- como acessar no navegador
- endpoints disponíveis
- limitações atuais
- próximos passos
```

---

## 9. Ordem operacional ideal

Se quiser minimizar erro, siga esta ordem exata:

```text
PASSO 1  -> subir arquivos
PASSO 2  -> mandar prompt mestre
PASSO 3  -> mandar pedido do backend
PASSO 4  -> mandar pedido do frontend
PASSO 5  -> mandar auditoria de consistência
PASSO 6  -> mandar README final
PASSO 7  -> baixar o repositório gerado
PASSO 8  -> rodar localmente com docker-compose up
```

---

## 10. Como saber se a IA fez certo

### Sinais de que fez certo
- existe `docker-compose.yml`
- existe `.env.example`
- backend sobe
- frontend sobe
- API responde
- navegador abre dashboard
- há separação entre adapters, parsers e api
- há tabela/estrutura para eventos de dividendos

### Sinais de que fez errado
- entregou só pseudocódigo
- criou tudo em um arquivo só
- não conectou frontend e backend
- não preparou banco
- não deixou comando de execução
- escreveu arquitetura bonita mas não implementou

---

## 11. Como testar no seu PC

Depois de baixar o projeto gerado, rode:

```bash
docker-compose up --build
```

Depois tente abrir algo como:

```text
http://localhost:3000
```

ou

```text
http://localhost:5173
```

e também teste:

```text
http://localhost:8000/docs
```

Se abrir a documentação do FastAPI, o backend está vivo.

---

## 12. Checklist de aceite

Considere aprovado apenas se houver:

- [ ] repositório completo
- [ ] backend FastAPI funcionando
- [ ] PostgreSQL configurado
- [ ] docker-compose funcional
- [ ] frontend React funcionando
- [ ] dashboard abrindo no navegador
- [ ] endpoint de eventos futuros
- [ ] endpoint de eventos acionáveis
- [ ] parser/classificador inicial implementado
- [ ] README de execução
- [ ] separação entre evento oficial e estimado

---

## 13. Prompt de correção, se vier meia-boca

Se ele devolver algo fraco, mande isto:

```text
A entrega veio incompleta.

Corrija agora com foco em execução real, não em explicação.
Quero:

- código implementado
- arquivos completos
- integração entre backend, banco e frontend
- docker-compose funcional
- README de execução
- correção de inconsistências

Não resuma. Não entregue só estrutura. Entregue código utilizável.
```

---

## 14. Prompt de continuação, se travar no meio

```text
Continue a partir do ponto atual sem recomeçar o projeto.
Complete os arquivos faltantes e finalize o MVP funcional.
```

---

## 15. Melhor estratégia prática

A forma mais eficiente é esta:

```text
1. subir tudo
2. mandar prompt mestre
3. pedir backend
4. pedir frontend
5. pedir auditoria
6. pedir README final
```

Não peça “faz tudo” de forma solta.
Peça em blocos grandes, mas com destino claro.

---

## 16. Resultado final esperado

No fim, você deve ter:

```text
um aplicativo web local
que abre no navegador
coleta dados de proventos
normaliza eventos
salva em banco
e mostra tudo num dashboard simples
```

---

## 17. Resumo curtíssimo para uso imediato

Se quiser a versão seca, use esta ordem:

```text
Suba README_MASTER.md + IMPLEMENTATION_PLAN.md + starter_code/
Cole o prompt mestre
Peça backend
Peça frontend
Peça auditoria
Baixe o repo
Rode docker-compose up --build
Abra no navegador
```
