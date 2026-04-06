from fastapi import FastAPI
from app.database import Base, engine


app = FastAPI(title="Micro Goals API", version="0.1.0")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to Micro Goals API"}