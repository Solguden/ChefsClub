from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.core.database import Base

class Guests(Base):
    __tablename__ = "guests"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id",ondelete="CASCADE"))
    
    tenant: Mapped["Tenants"] = relationship(back_populates="guests")
    
    allergies: Mapped[list["Allergies"]] = relationship(
        secondary="guest_allergies", 
        back_populates="guests"
    )
    
    dinner_appearances: Mapped[List["DinnerParticipants"]] = relationship(back_populates="guest")