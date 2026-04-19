from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class GoalCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: datetime


class GoalUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|paused)$")


class GoalResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    deadline: datetime
    status: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True