from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.schemas.micro_task import MicroTaskResponse, MicroTaskUpdate, GoalProgress
from app.models.micro_task import MicroTask
from app.utils.dependencies import get_current_user
from app.services.decomposition import decompose_goal, rebalance_goal

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("/", response_model=GoalResponse, status_code=201)
def create_goal(
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_goal = Goal(
        title=goal_data.title,
        description=goal_data.description,
        deadline=goal_data.deadline,
        user_id=current_user.id,
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    decompose_goal(new_goal, db)
    return new_goal


@router.get("/", response_model=List[GoalResponse])
def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
    return goals


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id,
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id,
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    if goal_data.title is not None:
        goal.title = goal_data.title
    if goal_data.description is not None:
        goal.description = goal_data.description
    if goal_data.deadline is not None:
        goal.deadline = goal_data.deadline
    if goal_data.status is not None:
        goal.status = goal_data.status

    db.commit()
    db.refresh(goal)

    return goal


@router.delete("/{goal_id}", status_code=204)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id,
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.delete(goal)
    db.commit()


@router.get("/{goal_id}/tasks", response_model=List[MicroTaskResponse])
def get_goal_tasks(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id,
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    tasks = db.query(MicroTask).filter(
        MicroTask.goal_id == goal_id,
    ).order_by(MicroTask.day_number).all()

    return tasks


@router.patch("/{goal_id}/tasks/{task_id}", response_model=MicroTaskResponse)
def update_task(
    goal_id: int,
    task_id: int,
    task_data: MicroTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id,
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    task = db.query(MicroTask).filter(
        MicroTask.id == task_id,
        MicroTask.goal_id == goal_id,
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_completed = task_data.is_completed

    if task_data.is_completed:
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None

    db.commit()
    db.refresh(task)

    return task


@router.get("/{goal_id}/progress", response_model=GoalProgress)
def get_goal_progress(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id,
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    tasks = db.query(MicroTask).filter(
        MicroTask.goal_id == goal_id,
    ).all()

    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.is_completed])
    remaining_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress_percentage = round((completed_tasks / total_tasks) * 100, 1)
    else:
        progress_percentage = 0.0

    now = datetime.utcnow()
    days_since_start = (now - goal.created_at).days + 1
    current_day = min(days_since_start, total_tasks)
    days_remaining = max(0, (goal.deadline - now).days)

    return GoalProgress(
        goal_id=goal.id,
        goal_title=goal.title,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        progress_percentage=progress_percentage,
        current_day=current_day,
        days_remaining=days_remaining,
    )

@router.post("/{goal_id}/rebalance", response_model=List[MicroTaskResponse])
def rebalance_goal_tasks(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id,
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    rebalanced_tasks = rebalance_goal(goal, db)

    return rebalanced_tasks
