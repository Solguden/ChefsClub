from app.core.database import engine, SessionLocal, Base
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
    birthday="25-10-1996",
    preferences=TenantPreferences()
    )
db.add(user)
db.commit()

# 3️⃣ Hent alle brugere for at bekræfte
users = db.query(Tenants).all()
print(users)

db.close()
