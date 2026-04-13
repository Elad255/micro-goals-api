from fastapi import FastAPI, Depends
from app.database import Base, engine
from app.routers import auth
from app.models.user import User
from app.utils.dependencies import get_current_user

app = FastAPI(title="Micro Goals API", version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to Micro Goals API"}


@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }