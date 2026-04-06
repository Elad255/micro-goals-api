from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class MicroTask(Base):
    __tablename__ = "micro_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    day_number = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)

    goal = relationship("Goal", back_populates="micro_tasks")