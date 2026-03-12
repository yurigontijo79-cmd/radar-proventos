"""Parser inicial de documentos de proventos.

Aqui estamos usando a abordagem mais honesta para um MVP:
- regex
- palavras-chave
- heurística simples

Nada de fingir que a primeira versão é mágica.
Primeiro fazemos funcionar. Depois refinamos.
"""

from __future__ import annotations

import re
from datetime import datetime

MONEY_RE = re.compile(r"R\$\s*([0-9]{1,3}(?:\.[0-9]{3})*,[0-9]+)")
DATE_RE = re.compile(r"([0-9]{2}/[0-9]{2}/[0-9]{4})")


def parse_brl_money(raw: str) -> float:
    """Converte moeda brasileira para float.

    Exemplo:
    '1.234,56' -> 1234.56
    """
    cleaned = raw.replace(".", "").replace(",", ".")
    return float(cleaned)


def parse_br_date(raw: str):
    return datetime.strptime(raw, "%d/%m/%Y").date()


def detect_event_type(text: str) -> str:
    lowered = text.lower()
    if "juros sobre capital próprio" in lowered or "jcp" in lowered:
        return "JCP"
    if "dividendo" in lowered:
        return "DIVIDEND"
    return "UNKNOWN"


def extract_first_money(text: str) -> float | None:
    match = MONEY_RE.search(text)
    if not match:
        return None
    return parse_brl_money(match.group(1))


def extract_dates(text: str) -> list:
    return [parse_br_date(raw) for raw in DATE_RE.findall(text)]


def parse_dividend_document(text: str) -> dict | None:
    """Extrai uma estrutura mínima de evento a partir de texto bruto.

    Heurística simples:
    - pega o primeiro valor monetário como valor por ação;
    - tenta capturar até três datas na ordem em que aparecem.

    Isso não é perfeito, mas já permite validar o pipeline end-to-end.
    """
    amount = extract_first_money(text)
    if amount is None:
        return None

    dates = extract_dates(text)
    event_type = detect_event_type(text)

    payload = {
        "event_type": event_type,
        "amount_per_share": amount,
        "announcement_date": dates[0] if len(dates) > 0 else None,
        "record_date": dates[1] if len(dates) > 1 else None,
        "payment_date": dates[2] if len(dates) > 2 else None,
    }
    return payload
