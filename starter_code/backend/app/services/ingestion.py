from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path
import sys

from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.dividend_event import DividendEvent
from app.models.source_document import SourceDocument
from app.services.parser import parse_dividend_document
from app.services.status_classifier import classify_status

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from scrapers.ri_adapter import fetch_ri_documents  # noqa: E402

DIVIDEND_TERMS = ["dividendo", "dividendos", "jcp", "juros sobre capital", "provento", "proventos"]


def _classification_score(text: str, title: str | None) -> float:
    probe = f"{title or ''} {text[:12000]}".lower()
    hits = sum(1 for term in DIVIDEND_TERMS if term in probe)
    return round(min(1.0, hits / 3), 2)


def _content_hash(text: str) -> str:
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _save_raw_document(company_ticker: str, doc_hash: str, text: str) -> str:
    raw_dir = PROJECT_ROOT / "data" / "raw_documents"
    raw_dir.mkdir(parents=True, exist_ok=True)
    file_path = raw_dir / f"{company_ticker}_{doc_hash[:16]}.txt"
    if not file_path.exists():
        file_path.write_text(text, encoding="utf-8")
    return str(file_path.relative_to(PROJECT_ROOT))


def _already_exists(db: Session, company_id: int, doc_hash: str) -> SourceDocument | None:
    return (
        db.query(SourceDocument)
        .filter(SourceDocument.company_id == company_id, SourceDocument.content_hash == doc_hash)
        .first()
    )


def _official_event_exists(db: Session, company_id: int, payload: dict) -> bool:
    query = db.query(DividendEvent).filter(
        DividendEvent.company_id == company_id,
        DividendEvent.event_type == payload["event_type"],
        DividendEvent.amount_per_share == payload["amount_per_share"],
        DividendEvent.record_date == payload.get("record_date"),
        DividendEvent.payment_date == payload.get("payment_date"),
        DividendEvent.confidence == "official",
        DividendEvent.is_estimated.is_(False),
    )
    return db.query(query.exists()).scalar()


def ingest_ri_documents(db: Session) -> dict:
    companies = db.query(Company).filter(Company.active.is_(True), Company.ri_url.is_not(None)).all()

    summary = {
        "companies_scanned": len(companies),
        "documents_fetched": 0,
        "documents_saved": 0,
        "candidate_documents": 0,
        "official_events_created": 0,
    }

    for company in companies:
        documents = fetch_ri_documents(company.ri_url)
        summary["documents_fetched"] += len(documents)

        for doc in documents:
            raw_text = doc["raw_text"]
            doc_hash = _content_hash(raw_text)

            if _already_exists(db, company.id, doc_hash):
                continue

            score = _classification_score(raw_text, doc.get("title"))
            is_candidate = score >= 0.34
            raw_path = _save_raw_document(company.ticker, doc_hash, raw_text)
            enriched_text = f"[raw_path={raw_path}]\n{raw_text}"

            source_document = SourceDocument(
                company_id=company.id,
                source_type=doc.get("source_type", "ri"),
                url=doc["url"],
                title=doc.get("title"),
                published_at=doc.get("published_at"),
                raw_text=enriched_text,
                content_hash=doc_hash,
                is_dividend_candidate=is_candidate,
                classification_score=score,
            )
            db.add(source_document)
            db.flush()

            summary["documents_saved"] += 1
            if is_candidate:
                summary["candidate_documents"] += 1

            payload = parse_dividend_document(raw_text) if is_candidate else None
            if not payload or payload["event_type"] not in {"DIVIDEND", "JCP"}:
                continue

            if _official_event_exists(db, company.id, payload):
                continue

            event = DividendEvent(
                company_id=company.id,
                source_document_id=source_document.id,
                ticker=company.ticker,
                event_type=payload["event_type"],
                amount_per_share=payload["amount_per_share"],
                announcement_date=payload.get("announcement_date"),
                record_date=payload.get("record_date"),
                ex_date=payload.get("ex_date"),
                payment_date=payload.get("payment_date"),
                status=classify_status(date.today(), payload.get("record_date"), payload.get("ex_date"), payload.get("payment_date")),
                confidence="official",
                is_estimated=False,
            )
            db.add(event)
            summary["official_events_created"] += 1

    db.commit()
    return summary
