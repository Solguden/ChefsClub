from fastapi import FastAPI
from app.api.tenants_api import router as tenants_router
from app.api.dinners_api import router as dinners_router
from app.api.guests_api import router as guests_router
from app.jobs.dinner.dinner_jobs import generate_monthly_dinners
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler.add_job(generate_monthly_dinners, "cron", day=28,hour=3)
    scheduler.start()
    yield
    scheduler.shutdown()
    
app = FastAPI(title="ChefsClub API")

@app.get("/test")
def test_connection():
    return {"status": "Det virker!"}

app.include_router(tenants_router, prefix="/api")
app.include_router(dinners_router, prefix="/api")
app.include_router(guests_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "ChefsClub API is running!"}