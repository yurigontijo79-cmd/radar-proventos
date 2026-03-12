from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dividend_event import DividendEvent
from app.schemas.dividend_event import DividendEventRead
from app.services.status_classifier import classify_status

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[DividendEventRead])
def list_events(db: Session = Depends(get_db)):
    return db.query(DividendEvent).order_by(DividendEvent.payment_date.asc()).all()


@router.get("/upcoming", response_model=list[DividendEventRead])
def list_upcoming_events(db: Session = Depends(get_db)):
    today = date.today()
    return (
        db.query(DividendEvent)
        .filter(or_(DividendEvent.record_date >= today, DividendEvent.payment_date >= today))
        .order_by(DividendEvent.record_date.asc().nulls_last(), DividendEvent.payment_date.asc().nulls_last())
        .all()
    )


@router.get("/predicted", response_model=list[DividendEventRead])
def list_predicted_events(db: Session = Depends(get_db)):
    return (
        db.query(DividendEvent)
        .filter(
            or_(
                DividendEvent.is_estimated.is_(True),
                DividendEvent.confidence.in_(["estimated", "inferred"]),
            )
        )
        .order_by(DividendEvent.payment_date.asc().nulls_last())
        .all()
    )


@router.post("/recompute-status")
def recompute_status(db: Session = Depends(get_db)):
    today = date.today()
    events = db.query(DividendEvent).all()
    for event in events:
        event.status = classify_status(today, event.record_date, event.ex_date, event.payment_date)
    db.commit()
    return {"updated": len(events)}
