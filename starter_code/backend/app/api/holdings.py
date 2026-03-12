from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.holding import Holding
from app.schemas.holding import HoldingCreate, HoldingRead

router = APIRouter(prefix="/holdings", tags=["holdings"])


@router.get("", response_model=list[HoldingRead])
def list_holdings(db: Session = Depends(get_db)):
    return db.query(Holding).order_by(Holding.ticker.asc()).all()


@router.post("", response_model=HoldingRead)
def create_holding(payload: HoldingCreate, db: Session = Depends(get_db)):
    holding = Holding(**payload.model_dump())
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return holding
