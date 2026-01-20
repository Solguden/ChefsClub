from fastapi import FastAPI, Depends, HTTPException, APIRouter, status,Response
from app.models import Tenants, TenantPreferences, Allergies
from app.api import UpdateTenantAllergiesRequest
from app.schemas.tenants_schema import TenantCreate, TenantUpdate, TenantDeactivate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from sqlalchemy.orm import selectinload 
from app.core.database import get_db

router = APIRouter()

@router.get("/tenants")
async def list_tenants(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenants))
    tenants = result.scalars().all()
    
    if not tenants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No tenants found")
        
    return tenants

@router.post("/tenants")
async def create_tenant(tenant: TenantCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenants).filter(Tenants.room_number == tenant.room_number, Tenants.active == True))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail=f"Active tenant on selected Room Number: {existing.room_number} already exists.")
    
    db_tenant = Tenants(
        email=tenant.email,
        room_number=tenant.room_number,
        name=tenant.name,
        birthday=tenant.birthday,
        preferences=TenantPreferences()
    )
    
    db.add(db_tenant)
    await db.commit() 
    await db.refresh(db_tenant) 
    return db_tenant

@router.put("/tenants")
async def update_tenant(tenant: TenantUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenants).filter(Tenants.id == tenant.id))
    existing = result.scalar_one_or_none()
    
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
    
    await db.commit()
    await db.refresh(existing)
    return existing

@router.put("/tenants/deactivate")
async def deactivate_tenant(tenant: TenantDeactivate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenants).filter(Tenants.id == tenant.id, Tenants.active == True))
    existing = result.scalar_one_or_none()
    
    if not existing:
        raise HTTPException(status_code=404, detail=f"Active tenant for id {tenant.id} and room number: {tenant.room_number} not found.")
    
    existing.active = False
    
    await db.commit()
    await db.refresh(existing)
    return existing

@router.put("tenants/allergies")
async def put_guest_allergies(request: UpdateTenantAllergiesRequest, db: AsyncSession = Depends(get_db)):
    query1 = (
        select(Tenants)
        .where(Tenants.id == request.tenant_id)
        .options(selectinload(Tenants.allergies))
    )
    result = await db.execute(query1)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Tenant with id: {request.tenant_id} not found")
        
    difference = set(request.allergies) - set(tenant.allergies)
    
    stmt = (
        select(Allergies)
        .where(Allergies.id.in_(difference))
    )
    result = await db.execute(stmt)
    allergies_found = result.scalars().all()
    
    for a in allergies_found:
        tenant.allergies.append(a)
        
    await db.commit()
    
    return Response(
        content=None,
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )