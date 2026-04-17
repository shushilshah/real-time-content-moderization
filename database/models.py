# Auto-generated file
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.db import Base

class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True)
    text = Column(String, nullable=False)
    toxicity = Column(Float, nullable=False)
    label = Column(String, nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
