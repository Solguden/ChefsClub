from datetime import date
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Date, Enum as SQLEnum
from app.core.database import Base
from app.models.dinners.dinner_participants_model import DinnerParticipants

class DinnerStatus(Enum):
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    COMPLETE = "complete"
    CANCELLED = "cancelled"
    
class DinnerType(Enum):
    NORMAL = "normal"
    SPECIAL = "special"

class Dinners(Base):
    __tablename__ = "dinners"
    date: Mapped[date] = mapped_column(Date, primary_key=True)
    meal: Mapped[str] = mapped_column(String, default="TBD")
    status: Mapped[DinnerStatus] = mapped_column(
        SQLEnum(DinnerStatus), 
        default=DinnerStatus.UNASSIGNED,
        nullable=False
    )
    type: Mapped[DinnerType] = mapped_column(
        SQLEnum(DinnerType), 
        default=DinnerType.NORMAL,
        nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=True)
    
    images: Mapped[Optional[List["DinnerImages"]]] = relationship(
        back_populates="dinner",
        cascade="all, delete-orphan"
    )
    
    participants: Mapped[Optional[List[DinnerParticipants]]] = relationship(
        back_populates="dinner",
        cascade="all, delete-orphan"
    )
    
    