from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).order_by(Company.ticker.asc()).all()


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    response: Response,
    idempotent: bool = Query(False, description="Se true, retorna empresa existente quando ticker já existe."),
    db: Session = Depends(get_db),
):
    existing = db.query(Company).filter(Company.ticker == payload.ticker).first()
    if existing:
        if idempotent:
            response.status_code = status.HTTP_200_OK
            return existing
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ticker '{payload.ticker}' já cadastrado")

    company = Company(**payload.model_dump())
    db.add(company)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(Company).filter(Company.ticker == payload.ticker).first()
        if idempotent and existing:
            response.status_code = status.HTTP_200_OK
            return existing
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ticker '{payload.ticker}' já cadastrado")

    db.refresh(company)
    return company
