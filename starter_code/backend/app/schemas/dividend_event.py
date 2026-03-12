from datetime import date

from pydantic import BaseModel


class DividendEventRead(BaseModel):
    id: int
    ticker: str
    event_type: str
    amount_per_share: float
    announcement_date: date | None = None
    record_date: date | None = None
    ex_date: date | None = None
    payment_date: date | None = None
    status: str | None = None
    confidence: str
    is_estimated: bool

    class Config:
        from_attributes = True
