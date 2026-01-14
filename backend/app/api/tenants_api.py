from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.tenant_preferences_model import TenantPreferences
from app.models.tenants_model import Tenants
from app.schemas.tenants_schema import TenantCreate, TenantUpdate, TenantDeactivate

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tenants")
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenants).all()

@app.post("/tenants")
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    existing = db.query(Tenants).filter(Tenants.room_number == tenant.room_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room number already exists")
    
    db_tenant = Tenants(
        email=tenant.email,
        room_number=tenant.room_number,
        name=tenant.name,
        birthday=tenant.birthday,
        preferences=TenantPreferences()
    )
    
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

@app.put("/tenants")
def update_tenant(tenant: TenantUpdate, db: Session = Depends(get_db)):
    existing = db.query(Tenants).filter(Tenants.id == tenant.id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Id doesnt exist")
    
    if tenant.name is not None:
        existing.name = tenant.name
    if tenant.email is not None:
        existing.email = tenant.email
    if tenant.room_number is not None:
        existing.room_number = tenant.room_number
    if tenant.birthday is not None:
        existing.birthday = tenant.birthday
    
    db.commit()
    db.refresh(existing)
    return existing

@app.put("/tenants/preferences")
def update_tenant(tenant: TenantUpdate, db: Session = Depends(get_db)):
    existing = db.query(Tenants).filter(Tenants.id == tenant.id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Id doesnt exist")
    
    if tenant.name is not None:
        existing.name = tenant.name
    if tenant.email is not None:
        existing.email = tenant.email
    if tenant.room_number is not None:
        existing.room_number = tenant.room_number
    if tenant.birthday is not None:
        existing.birthday = tenant.birthday
    
    db.commit()
    db.refresh(existing)
    return existing

# @app.put("/tenants/deactivate")
# def update_tenant(tenant: TenantUpdate, db: Session = Depends(get_db)):
#     existing = db.query(Tenants).filter(Tenants.room_number == tenant.room_number).first()
#     if not existing:
#         raise HTTPException(status_code=404, detail="Room number doesnt exist")
    
#     if tenant.name is not None:
#         existing.name = tenant.name
#     if tenant.birthday is not None:
#         existing.birthday = tenant.birthday
    
#     db.commit()
#     db.refresh(existing)
#     return existing
    