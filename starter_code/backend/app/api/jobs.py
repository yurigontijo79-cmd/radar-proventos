from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ingestion import ingest_ri_documents

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/run-ingestion")
def run_ingestion(db: Session = Depends(get_db)):
    summary = ingest_ri_documents(db)
    return {"message": "Ingestão de RI concluída.", "summary": summary}


@router.post("/run-predictions")
def run_predictions():
    return {"message": "Job de previsão disparado (stub inicial)."}
