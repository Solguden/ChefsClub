from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response
from app.models import Guests, GuestAllergies, Tenants, Allergies
from app.api import CreateGuestRequest, UpdateGuestAllergiesRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from sqlalchemy.orm import selectinload
from app.core.database import get_db

router = APIRouter()

@router.post("/guests",response_model=None)
async def create_guest(request: CreateGuestRequest, db: AsyncSession = Depends(get_db)):
    query1 = (
        select(Tenants)
        .where(Tenants.id == request.tenant_id)
        .options(selectinload(Tenants.guests))
    )
    result = await db.execute(query1)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=400, detail=f"Active tenant on for requested id: {request.tenant_id} doesn't exists.")
    
    exists = next((True for g in tenant.guests if g.name == request.name), False)
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=(f"Guest with name {request.name} already exists for tenant with id: {request.tenant_id}"))    
    
    tenant.guests.append(
        Guests(
            tenant_id = request.tenant_id,
            name = request.name
        )
    )
    await db.commit()
    
    return Response(
        content=None,
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )
    
@router.put("guests/allergies")
async def put_guest_allergies(request: UpdateGuestAllergiesRequest, db: AsyncSession = Depends(get_db)):
    query1 = (
        select(Guests)
        .where(Guests.id == request.guest_id)
        .options(selectinload(Guests.allergies))
    )
    result = await db.execute(query1)
    guest = result.scalar_one_or_none()
    
    if not guest:
        raise HTTPException(status_code=404, detail=f"Guest with id: {request.guest_id} not found")
        
    difference = set(request.allergies) - set(guest.allergies)
    
    stmt = (
        select(Allergies)
        .where(Allergies.id.in_(difference))
    )
    result = await db.execute(stmt)
    allergies_found = result.scalars().all()
    
    for a in allergies_found:
        guest.allergies.append(a)
        
    await db.commit()
    
    return Response(
        content=None,
        status_code=200,
        headers=None,
        media_type=None,
        background=None,
    )