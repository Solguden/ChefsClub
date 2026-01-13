from core.database import engine, SessionLocal, Base
from models.tenants_model import Tenants

# 1️⃣ Opret tabeller (hvis de ikke findes)
Base.metadata.create_all(bind=engine)

# 2️⃣ Tilføj en test-bruger
db = SessionLocal()
user = Tenants(
    room_number="206-2",
    name="Jeppe",
    birthday="25-10-1996"
    )
db.add(user)
db.commit()

# 3️⃣ Hent alle brugere for at bekræfte
users = db.query(Tenants).all()
print(users)

db.close()
