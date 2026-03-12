from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dividend_event import DividendEvent
from app.models.holding import Holding

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    events = db.query(DividendEvent).count()
    holdings = db.query(Holding).count()
    return {
        "events": events,
        "holdings": holdings,
    }


@router.get("/cashflow")
def dashboard_cashflow(db: Session = Depends(get_db)):
    today = date.today()
    holdings = {h.ticker: h for h in db.query(Holding).all()}
    events = (
        db.query(DividendEvent)
        .filter(DividendEvent.payment_date.is_not(None), DividendEvent.payment_date >= today)
        .order_by(DividendEvent.payment_date.asc())
        .all()
    )

    rows = []
    total = 0.0
    for event in events:
        holding = holdings.get(event.ticker)
        if not holding:
            continue
        expected = round(holding.quantity * event.amount_per_share, 2)
        total += expected
        rows.append(
            {
                "ticker": event.ticker,
                "payment_date": event.payment_date,
                "amount_per_share": event.amount_per_share,
                "quantity": holding.quantity,
                "expected_cash": expected,
                "status": event.status,
            }
        )

    return {"total_expected_cash": round(total, 2), "items": rows}
