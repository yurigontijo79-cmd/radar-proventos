from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String

from app.core.database import Base


class DividendEvent(Base):
    __tablename__ = "dividend_events"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    source_document_id = Column(Integer, ForeignKey("source_documents.id"), nullable=True, index=True)
    ticker = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    amount_per_share = Column(Float, nullable=False)
    announcement_date = Column(Date, nullable=True)
    record_date = Column(Date, nullable=True)
    ex_date = Column(Date, nullable=True)
    payment_date = Column(Date, nullable=True)
    status = Column(String, nullable=True)
    confidence = Column(String, default="official", nullable=False)
    is_estimated = Column(Boolean, default=False, nullable=False)
