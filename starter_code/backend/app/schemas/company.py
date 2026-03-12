from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    ticker: str
    sector: str | None = None
    cvm_code: str | None = None
    ri_url: str | None = None


class CompanyRead(CompanyCreate):
    id: int
    active: bool

    class Config:
        from_attributes = True
