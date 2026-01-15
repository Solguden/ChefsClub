from typing import List
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String, Boolean, ForeignKey, Integer
from app.core.database import Base

class TenantPreferences(Base):
    __tablename__ = "tenant_preferences"
    
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    available_weekdays : Mapped[List[int]] = mapped_column(ARRAY(Integer), default=[0,1,2,3,6])
    available_months : Mapped[List[int]] = mapped_column(ARRAY(Integer), default=[0,1,2,3,4,5,6,7,8,9,10,11,12])
    unavailable_dates_current_month : Mapped[List[int]] = mapped_column(ARRAY(Integer), default=[]) #Remember to reset every month
    
    tenant: Mapped["Tenants"] = relationship(back_populates="preferences")
    