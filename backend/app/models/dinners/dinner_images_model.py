from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String, Boolean, Date, ForeignKey
from app.core.database import Base

class DinnerImages(Base):
    __tablename__ = "dinner_images"
    date: Mapped[date] = mapped_column(
        ForeignKey("dinners.date", ondelete="CASCADE"),
        primary_key=True
    )
    
    images: Mapped[List[str]]= mapped_column(ARRAY(String), default=[])

    dinner: Mapped["Dinners"] = relationship(back_populates="images")