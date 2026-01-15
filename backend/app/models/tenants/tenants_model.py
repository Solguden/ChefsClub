from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Date
from app.core.database import Base

class Tenants(Base):
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_number: Mapped[str] = mapped_column(String(5))
    email: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    birthday: Mapped[date] = mapped_column(Date())
    active: Mapped[bool] = mapped_column(Boolean, unique=False, default=True)
    
    preferences: Mapped[Optional["TenantPreferences"]] = relationship(
        back_populates="tenant",
        cascade="all, delete-orphan"
    )
    
    participations: Mapped[List["DinnerParticipants"]] = relationship(
        back_populates="participant",
        cascade="all, delete-orphan"
    )
    
    guests: Mapped[List["Guests"]] = relationship(
        back_populates="tenant",
        cascade="all, delete-orphan"
    )