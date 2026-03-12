from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    source_type = Column(String, nullable=False, default="ri")
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    published_at = Column(Date, nullable=True)
    raw_text = Column(Text, nullable=False)
    content_hash = Column(String, nullable=False, index=True)
    is_dividend_candidate = Column(Boolean, nullable=False, default=False)
    classification_score = Column(Float, nullable=False, default=0.0)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
