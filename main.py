from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from db import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
