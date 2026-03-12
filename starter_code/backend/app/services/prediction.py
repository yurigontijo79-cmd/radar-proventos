"""Motor simplificado de previsão.

A ideia aqui não é prometer clarividência.
É apenas organizar um score inicial com base em regularidade e payout.
Depois esse módulo pode crescer com dados financeiros mais robustos.
"""


def estimate_dividend(lpa: float, payout: float) -> float:
    return round(lpa * payout, 4)


def prediction_score(
    regularity: float,
    timing: float,
    payout_stability: float,
    earnings_strength: float,
    cash_strength: float,
) -> float:
    score = (
        0.35 * regularity
        + 0.25 * timing
        + 0.20 * payout_stability
        + 0.10 * earnings_strength
        + 0.10 * cash_strength
    )
    return round(score, 4)
