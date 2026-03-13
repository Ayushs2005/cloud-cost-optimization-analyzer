from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class CostData(Base):
    __tablename__ = "cost_data"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String)
    cost = Column(Float)
    usage_date = Column(Date)
