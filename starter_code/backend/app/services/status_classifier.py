"""Classificador temporal de eventos.

Esse cara responde à pergunta prática mais importante do app:
- ainda dá tempo?
- é o último dia?
- já garantiu, mas ainda não pagou?
- já pagou?

Sem isso, a tela vira apenas catálogo bonito. Com isso, vira ferramenta.
"""

from datetime import date


def classify_status(today: date, record_date: date | None, ex_date: date | None, payment_date: date | None) -> str:
    if record_date and today < record_date:
        return "ainda_da_tempo"
    if record_date and today == record_date:
        return "ultimo_dia"
    if ex_date and payment_date and ex_date <= today < payment_date:
        return "pagamento_pendente"
    if payment_date and today >= payment_date:
        return "pago"
    return "indefinido"
