from datetime import date
from app.core.database import engine, SessionLocal, Base
from app.models import DinnerImages, DinnerParticipants, ParticipantRole, DinnerStatus, Dinners, TenantPreferences, Tenants, Allergies, TenantAllergies, GuestAllergies, Guests

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
        
        allergies = [
            "Gluten", "Lactose", "Nuts", "Vegetarian", "Vegan", "Pescetar", "No fish", "No pig", "No cow", "No lamb", "No alcohol" 
        ]
        allergiesObjects = {}
        
        for name in allergies:
            a = Allergies(name=name)
            db.add(a)
            allergiesObjects[name] = a

        await db.flush() 
        
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
            
        guest1 = Guests(name="Mormor",tenant_id=user2.id)
        guest1.allergies.append(allergiesObjects["Lactose"])
        user2.guests.append(
            guest1
        )
        
        user2.allergies.append(allergiesObjects["Gluten"]
        )
         
        db.add_all([user1, user2])
        
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
        dinner_participant_3 = DinnerParticipants(
            dinner_date = dinner.date,
            participant_id = user2.id,
            guest_id = guest1.id,
            role = ParticipantRole.GUEST
        )
        
        dinner_images = DinnerImages(
            date = dinner.date,
            images = ["Image1", "Image2"]
        )

        db.add_all([dinner_participant_1, dinner_participant_2, dinner_images,dinner_participant_3])

        await db.commit()
        print("✅ Database er seedet asynkront!")
        
if __name__ == "__main__":
    asyncio.run(seed_data())