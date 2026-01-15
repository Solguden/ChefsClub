from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.core.database import Base

class GuestAllergies(Base):
    __tablename__ = "guest_allergies"
    guests_id : Mapped[int] = mapped_column(ForeignKey("guests.id"),primary_key=True)
    allergy_id : Mapped[int] = mapped_column(ForeignKey("allergies.id"),primary_key=True)