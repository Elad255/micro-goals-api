from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MicroTaskResponse(BaseModel):
    id: int
    title: str
    day_number: int
    is_completed: bool
    completed_at: Optional[datetime]
    created_at: datetime
    goal_id: int

    class Config:
        from_attributes = True


class MicroTaskUpdate(BaseModel):
    is_completed: bool


class GoalProgress(BaseModel):
    goal_id: int
    goal_title: str
    total_tasks: int
    completed_tasks: int
    remaining_tasks: int
    progress_percentage: float
    current_day: int
    days_remaining: int