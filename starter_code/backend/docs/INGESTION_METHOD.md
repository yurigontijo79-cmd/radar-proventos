# Método atual de ingestão oficial (RI beta)

## Objetivo
Entregar uma trilha mínima, auditável e executável para coletar anúncios oficiais em páginas de RI.

## Pipeline implementado
1. Seleciona empresas `active=true` e `ri_url` preenchido.
2. Busca links da página de RI contendo termos de proventos/dividendos/JCP.
3. Faz download do HTML desses links e extrai texto bruto.
4. Gera `content_hash` (sha256 de texto normalizado) para deduplicação por empresa.
5. Persiste `source_documents` com:
   - origem,
   - URL,
   - título,
   - data publicada (quando detectada),
   - texto bruto,
   - score de classificação,
   - flag de candidato.
6. Salva cópia local do texto bruto em `backend/data/raw_documents/` para auditoria manual.
7. Aplica parser heurístico (valor + datas + tipo DIVIDEND/JCP).
8. Persiste em `dividend_events` como evento oficial quando:
   - documento é candidato,
   - parse retornou tipo e valor,
   - não existe evento oficial com mesma chave lógica básica.

## Separação oficial vs estimado
- Ingestão RI grava apenas:
  - `confidence = "official"`
  - `is_estimated = false`
- Eventos estimados seguem responsabilidade do pipeline de previsão (ainda não implementado).

## Limitações conhecidas
- Sem parse robusto de PDF/planilhas.
- Sem classificação ML; apenas score por palavras-chave.
- Deduplicação de evento é mínima (chave lógica simplificada).
- Sem trilha completa de versionamento de documentos.
