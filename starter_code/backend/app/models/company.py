from sqlalchemy import Boolean, Column, Integer, String

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ticker = Column(String, unique=True, nullable=False, index=True)
    sector = Column(String, nullable=True)
    cvm_code = Column(String, nullable=True)
    ri_url = Column(String, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
