from sqlalchemy import  Column, Integer, String, Float, Date, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
   
class Base(DeclarativeBase): 
    pass
  
class DailyStats(Base):
    __tablename__ = "daily_stats"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=True)
    campaign_id = Column(String, nullable=True)
    spend = Column(Float, nullable=True)
    conversions = Column(Float, nullable=True)
    CPA = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("date", "campaign_id", name="uix_date_campaign"),
    )

