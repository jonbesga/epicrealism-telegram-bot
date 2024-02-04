from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float
)
from sqlalchemy.dialects import postgresql

Base = declarative_base()


class UsageHistory(Base):
    __tablename__ = "usage_history"
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Text, nullable=False)
    predict_time = Column(Float, nullable=False)
    prediction_id = Column(Text, nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False)

class TopUp(Base):
    __tablename__ = "topups"
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False)
