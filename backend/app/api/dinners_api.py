from datetime import date
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response
from app.models import Dinners, DinnerParticipants
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.core.database import get_db
from app.api import AddDinnerParticipantRequest
from app.models import ParticipantRole, Tenants
        
router = APIRouter()

@router.get("/dinners")
async def list_dinners(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dinners))
    dinners = result.scalars().all()
    
    if not dinners:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No dinners found")
        
    return dinners

@router.get("/dinners/{date}")
async def get_dinner(date: date, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dinners).filter(Dinners.date == date))
    dinner = result.scalar_one_or_none()
    
    if not dinner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No dinner found for date: {date}")
    
    return dinner

@router.get("/dinners/{date}/participants")
async def get_dinner_participants(date: date, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DinnerParticipants).filter(DinnerParticipants.dinner_date == date))
    return result.scalars().all()

@router.put("dinners/{date}/participants")
async def put_dinner_participants(request: AddDinnerParticipantRequest,  db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenants).filter(Tenants.id == request.tenant_id))
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Tenant with id: {request.tenant_id} not found")
    
    result2 = await db.execute(select(Dinners).filter(Dinners.date == request.date))
    dinner = result2.scalar_one_or_none()
    
    if not dinner:
        raise HTTPException(status_code=404, detail=f"Dinner for date: {request.date} not found")
    
    result3 = await db.execute(select(DinnerParticipants).filter(DinnerParticipants.dinner_date == request.date))
    participants = result3.scalars().all()
    
    if not participants:
        raise HTTPException(status_code=404, detail=f"Participants for Dinner for date: {request.date} not found")
    
    exists = next((True for p in participants if p.id == request.tenant_id), False)
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=(f"Tenant with {request.tenant_id} already exists for dinner with date: {dinner.date}"))    
    
    ##Todo have to be async
    dinner.participants.append(
        DinnerParticipants(
            dinner_date = dinner.date,
            participant_id = request.id, 
            role = ParticipantRole.Participant
        )
    )
    
    return Response(
        content=None,
        status_code=200,
        headers=None,
        media_type=None,
        background=None,
    )