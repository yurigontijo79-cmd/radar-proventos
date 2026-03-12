from pydantic import BaseModel


class HoldingCreate(BaseModel):
    ticker: str
    quantity: float
    avg_price: float | None = None
    source: str = "manual"


class HoldingRead(HoldingCreate):
    id: int

    class Config:
        from_attributes = True
