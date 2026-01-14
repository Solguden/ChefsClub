from datetime import date
from app.core.database import engine, SessionLocal, Base
from app.models.dinners.dinner_guests import DinnerGuests
from app.models.dinners.dinner_images_model import DinnerImages
from app.models.dinners.dinner_participants_model import DinnerParticipants, ParticipantRole
from app.models.dinners.dinners_model import Dinners
from app.models.tenant_preferences_model import TenantPreferences
from app.models.tenants_model import Tenants

# 1️⃣ Opret tabeller (hvis de ikke findes)
Base.metadata.create_all(bind=engine)

# 2️⃣ Tilføj en test-bruger
db = SessionLocal()
user = Tenants(
    email="jeppe3d@live.dk",
    room_number="206-2",
    name="Jeppe",
    birthday= date(year=1996,month=10,day=25),
    # preferences=TenantPreferences()
    )
# db.add(user)
# db.commit()

dinner = Dinners(
    date = date.today()
)
db.add(dinner)

dinner_participant_1 = DinnerParticipants(
    dinner_date = dinner.date,
    participant_id = 1,
    role = ParticipantRole.CHEF
)
db.add(dinner_participant_1)

dinner_participant_2 = DinnerParticipants(
    dinner_date = dinner.date,
    participant_id = 2,
    role = ParticipantRole.PARTICIPANT
)
db.add(dinner_participant_2)

dinner_images = DinnerImages(
    date = dinner.date,
    images = ["Image1","Image2"]
)
db.add(dinner_images)

guest = DinnerGuests(
    friend_of = 2
)
db.add(guest)
db.commit()


# 3️⃣ Hent alle brugere for at bekræfte
users = db.query(Tenants).all()
print(users)

db.close()
