from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Date
from app.core.database import Base
from app.models.dinners.dinner_participants_model import DinnerParticipants

class Dinners(Base):
    __tablename__ = "dinners"
    date: Mapped[date] = mapped_column(Date, primary_key=True)
    meal: Mapped[Optional[str]] = mapped_column(String, default="TBD")
    
    images: Mapped[Optional[List["DinnerImages"]]] = relationship(
        back_populates="dinner",
        cascade="all, delete-orphan"
    )
    
    participants: Mapped[Optional[List[DinnerParticipants]]] = relationship(
        back_populates="dinner",
        cascade="all, delete-orphan"
    )
    
    