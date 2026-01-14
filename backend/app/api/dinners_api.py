from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.dinners.dinners_model import Dinners

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/dinners")
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Dinners).all()