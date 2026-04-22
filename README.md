# Micro Goals API

![CI](https://github.com/Elad255/micro-goals-api/actions/workflows/ci.yml/badge.svg)

An intelligent REST API that helps users achieve their goals by automatically breaking them into daily micro-tasks with adaptive rebalancing. Built with FastAPI, PostgreSQL, and Docker.

## The Problem

92% of people fail their goals because they're too big and vague. "Learn Python" is overwhelming. But "Day 1: Research the best resources" is achievable.

## The Solution

Micro Goals API takes a big goal with a deadline and automatically decomposes it into a structured daily plan across 4 phases: Research, Building, Practice, and Review. As users track their progress, the system can rebalance remaining tasks to keep the plan achievable.


## Features

- **User Authentication** — Register, login, and JWT-based security for all endpoints
- **Goal Management** — Full CRUD (Create, Read, Update, Delete) for personal goals
- **AI Decomposition Engine** — Automatically generates daily micro-tasks organized into 4 learning phases
- **Progress Tracking** — Mark tasks complete, view real-time progress stats (percentage, completed/remaining tasks)
- **Adaptive Rebalancing** — Redistributes incomplete tasks across remaining days when users fall behind
- **CI/CD Pipeline** — Automated testing with GitHub Actions on every push
- **Dockerized** — Full Docker Compose setup with PostgreSQL and health checks


## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, SQLAlchemy ORM, Alembic migrations
- **Auth:** JWT tokens, bcrypt password hashing
- **Testing:** pytest with isolated test database
- **DevOps:** Docker, Docker Compose, GitHub Actions CI




## Project Structure

```
micro-goals/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py             # Environment settings
│   ├── database.py           # Database connection setup
│   ├── models/               # SQLAlchemy database models
│   │   ├── user.py
│   │   ├── goal.py
│   │   └── micro_task.py
│   ├── schemas/              # Pydantic validation schemas
│   │   ├── user.py
│   │   ├── goal.py
│   │   └── micro_task.py
│   ├── routers/              # API endpoint definitions
│   │   ├── auth.py
│   │   └── goals.py
│   ├── services/             # Business logic
│   │   └── decomposition.py
│   └── utils/                # Helper utilities
│       ├── security.py
│       ├── jwt.py
│       └── dependencies.py
├── tests/                    # Automated tests
│   ├── conftest.py
│   └── test_auth.py
├── .github/workflows/        # CI/CD pipeline
│   └── ci.yml
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```



## Getting Started

### Prerequisites

- Docker and Docker Desktop
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Elad255/micro-goals-api.git
cd micro-goals-api
```

2. Start the application:
```bash
docker compose up --build -d
```

3. Run database migrations:
```bash
docker compose exec api alembic upgrade head
```

4. The API is now running at `http://localhost:8000`

5. View the interactive API docs at `http://localhost:8000/docs`

### Running Tests

```bash
docker compose exec api pytest tests/ -v
```



## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/me` | Get current user info (requires auth) |

### Goals

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/goals/` | Create a new goal (auto-generates micro-tasks) |
| GET | `/goals/` | List all your goals |
| GET | `/goals/{id}` | Get a specific goal |
| PUT | `/goals/{id}` | Update a goal |
| DELETE | `/goals/{id}` | Delete a goal |

### Micro-Tasks & Progress

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/goals/{id}/tasks` | View all micro-tasks for a goal |
| PATCH | `/goals/{id}/tasks/{task_id}` | Mark a task as complete/incomplete |
| GET | `/goals/{id}/progress` | View progress stats for a goal |
| POST | `/goals/{id}/rebalance` | Rebalance incomplete tasks across remaining days |





## Example Usage

### 1. Register and Login

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword123"}'
```

### 2. Create a Goal (auto-generates micro-tasks)

```bash
curl -X POST http://localhost:8000/goals/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Python", "description": "Master FastAPI", "deadline": "2026-06-15T00:00:00"}'
```

### 3. View Your Daily Plan

```bash
curl -X GET http://localhost:8000/goals/1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Track Progress

```bash
# Mark a task complete
curl -X PATCH http://localhost:8000/goals/1/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}'

# View progress
curl -X GET http://localhost:8000/goals/1/progress \
  -H "Authorization: Bearer YOUR_TOKEN"
```




## How the Decomposition Engine Works

When a user creates a goal with a deadline, the system:

1. Calculates the number of days until the deadline
2. Divides those days into 4 phases:
   - **Research & Planning** (20%) — Explore resources, create a plan
   - **Building & Learning** (40%) — Learn concepts, practice fundamentals
   - **Practice & Deepening** (30%) — Advanced work, mini-projects
   - **Review & Polish** (10%) — Review, fill gaps, celebrate
3. Generates one micro-task per day from phase-specific templates
4. If the user falls behind, the rebalance endpoint redistributes remaining tasks evenly across remaining days

## License

This project is for educational and portfolio purposes.