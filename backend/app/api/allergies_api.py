from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from app.models import Allergies, GuestAllergies, TenantAllergies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.core.database import get_db

router = APIRouter()

#Put allergies for guest or participant