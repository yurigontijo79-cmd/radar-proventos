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
