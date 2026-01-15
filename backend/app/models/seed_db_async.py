from datetime import date
from app.core.database import engine, SessionLocal, Base
from app.models import DinnerImages, DinnerParticipants, ParticipantRole, DinnerStatus,DinnerGuests, Dinners, TenantPreferences, Tenants, Allergies, TenantAllergies

import asyncio
import sys
from datetime import date
from sqlalchemy import select
from app.core.database import engine, SessionLocal, Base

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        user1 = Tenants(
            email="jeppe3d@live.dk",
            room_number="206-2",
            name="Jeppe",
            birthday=date(1996, 10, 25),
            preferences = TenantPreferences()
        )
        user2 = Tenants(
            email="fabian@live.dk",
            room_number="206-1",
            name="Fabian",
            birthday=date(2002, 10, 28),
            preferences = TenantPreferences()
        )
        db.add_all([user1, user2])
        
        await db.flush() 
        
        allergies = [
            "Gluten", "Lactose", "Nuts", "Vegetarian", "Vegan", "Pescetar", "No fish", "No pig", "No cow", "No lamb", "No alcohol" 
        ]
        
        for a in allergies:
            db.add(Allergies(name=a))
            
        fabian_allergy1 = TenantAllergies(tenant_id=2,allergy_id=1)    
        fabian_allergy2 = TenantAllergies(tenant_id=2,allergy_id=2)    
        fabian_allergy3 = TenantAllergies(tenant_id=2,allergy_id=3)    
        db.add_all([fabian_allergy1,fabian_allergy2,fabian_allergy3])
        
        await db.flush() 

        dinner = Dinners(date=date.today(),status=DinnerStatus.ASSIGNED)
        db.add(dinner)
        await db.flush() 

        dinner_participant_1 = DinnerParticipants(
            dinner_date = dinner.date,
            participant_id = user1.id, 
            role = ParticipantRole.CHEF
        )
        dinner_participant_2 = DinnerParticipants(
            dinner_date = dinner.date,
            participant_id = user2.id,
            role = ParticipantRole.PARTICIPANT
        )
        
        dinner_images = DinnerImages(
            date = dinner.date,
            images = ["Image1", "Image2"]
        )

        guest = DinnerGuests(
            friend_of = user2.id 
        )

        db.add_all([dinner_participant_1, dinner_participant_2, dinner_images, guest])

        await db.commit()
        print("✅ Database er seedet asynkront!")
        
if __name__ == "__main__":
    asyncio.run(seed_data())