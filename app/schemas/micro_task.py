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