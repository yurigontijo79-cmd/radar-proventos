from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/run-ingestion")
def run_ingestion():
    return {"message": "Job de ingestão disparado (stub inicial)."}


@router.post("/run-predictions")
def run_predictions():
    return {"message": "Job de previsão disparado (stub inicial)."}
