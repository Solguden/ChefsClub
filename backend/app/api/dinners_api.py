from datetime import date
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from app.models import Dinners, DinnerParticipants
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.core.database import get_db
        
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

@router.get("/dinners/{date}/participants-and-guests")
async def get_dinner_participants(date: date, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DinnerParticipants).filter(DinnerParticipants.dinner_date == date))
    return result.scalars().all()