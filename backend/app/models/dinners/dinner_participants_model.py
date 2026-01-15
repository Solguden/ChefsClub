from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Enum as SQLEnum, CheckConstraint
from app.core.database import Base

class ParticipantRole(Enum):
    CHEF = "chef"
    PARTICIPANT = "participant"
    GUEST = "guest"

class DinnerParticipants(Base):
    __tablename__ = "dinner_participants"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    dinner_date : Mapped[date] = mapped_column(ForeignKey("dinners.date"))
    participant_id : Mapped[int] = mapped_column(ForeignKey("tenants.id"),nullable=True)
    guest_id : Mapped[Optional[int]] = mapped_column(ForeignKey("guests.id"),nullable=True)
    role: Mapped[ParticipantRole] = mapped_column(
        SQLEnum(ParticipantRole), 
        default=ParticipantRole.PARTICIPANT,
        nullable=False
    )
    
    signed_up_at : Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    dinner: Mapped["Dinners"] = relationship(back_populates="participants")
    participant: Mapped["Tenants"] = relationship(back_populates="participations")
    guest: Mapped["Guests"] = relationship(back_populates="dinner_appearances")
    
    # __table_args__ = (
    #     CheckConstraint(
    #         "(tenant_id IS NOT NULL AND guest_id IS NULL) OR (tenant_id IS NULL AND guest_id IS NOT NULL)",
    #         name="check_participant_type"
    #     ),
    # )

#TODO gennemtjek dinner_participants, tenants, guests, og allergies efter ny version af allergies.  