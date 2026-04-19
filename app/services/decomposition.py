from datetime import datetime, timedelta
from app.models.micro_task import MicroTask


PHASES = [
    {
        "name": "Research & Planning",
        "percentage": 0.20,
        "tasks": [
            "Research best resources for: {goal}",
            "Create a study plan for: {goal}",
            "Set up your workspace and tools for: {goal}",
            "Read introductory material about: {goal}",
            "Identify key milestones for: {goal}",
        ],
    },
    {
        "name": "Building & Learning",
        "percentage": 0.40,
        "tasks": [
            "Learn core concepts of: {goal}",
            "Practice fundamentals of: {goal}",
            "Build a small exercise for: {goal}",
            "Study intermediate topics in: {goal}",
            "Apply what you learned about: {goal}",
            "Work through a tutorial on: {goal}",
            "Solve practice problems for: {goal}",
            "Review and fix mistakes in: {goal}",
        ],
    },
    {
        "name": "Practice & Deepening",
        "percentage": 0.30,
        "tasks": [
            "Deep dive into advanced topics of: {goal}",
            "Build a mini-project related to: {goal}",
            "Practice under real conditions: {goal}",
            "Get feedback on your progress with: {goal}",
            "Refine your skills in: {goal}",
            "Challenge yourself with hard problems: {goal}",
        ],
    },
    {
        "name": "Review & Polish",
        "percentage": 0.10,
        "tasks": [
            "Review everything you learned about: {goal}",
            "Fill knowledge gaps in: {goal}",
            "Do a final practice run for: {goal}",
            "Celebrate your progress on: {goal}",
        ],
    },
]


def decompose_goal(goal, db):
    today = datetime.utcnow()
    days_remaining = (goal.deadline - today).days

    if days_remaining <= 0:
        days_remaining = 1

    tasks = []
    current_day = 1

    for phase in PHASES:
        phase_days = max(1, round(days_remaining * phase["percentage"]))
        phase_tasks = phase["tasks"]

        for i in range(phase_days):
            if current_day > days_remaining:
                break

            task_template = phase_tasks[i % len(phase_tasks)]
            task_title = task_template.format(goal=goal.title)

            micro_task = MicroTask(
                title=task_title,
                day_number=current_day,
                goal_id=goal.id,
            )

            db.add(micro_task)
            tasks.append(micro_task)
            current_day += 1

    db.commit()

    for task in tasks:
        db.refresh(task)

    return tasks