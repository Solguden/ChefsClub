from datetime import date
from app.core.database import engine, SessionLocal, Base
from app.models.dinners.dinner_guests import DinnerGuests
from app.models.dinners.dinner_images_model import DinnerImages
from app.models.dinners.dinner_participants_model import DinnerParticipants, ParticipantRole
from app.models.dinners.dinners_model import Dinners
from app.models.tenant_preferences_model import TenantPreferences
from app.models.tenants_model import Tenants

import asyncio
import sys
from datetime import date
from sqlalchemy import select
from app.core.database import engine, SessionLocal, Base
# ... dine andre imports ...

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def seed_data():
    # 1️⃣ Opret/Slet tabeller (Asynkron måde)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 2️⃣ Start en asynkron session
    async with SessionLocal() as db:
        # Opret brugere
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
        
        # NU flusher vi, så vi får deres ID'er fra databasen
        await db.flush() 

        # Opret middag
        dinner = Dinners(date=date.today())
        db.add(dinner)
        await db.flush() # Få middagens dato/ID klar

        # Tilføj deltagere (brug objekternes ID'er i stedet for 1 og 2)
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
            friend_of = user2.id # Fabian har en gæst med
        )

        db.add_all([dinner_participant_1, dinner_participant_2, dinner_images, guest])

        # Gem alt
        await db.commit()
        print("✅ Database er seedet asynkront!")
        
        
# Da det er et script, skal vi starte asyncio-loopet manuelt
if __name__ == "__main__":
    asyncio.run(seed_data())