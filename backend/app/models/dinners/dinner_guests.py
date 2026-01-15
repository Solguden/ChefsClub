# from datetime import date
# from typing import List, Optional
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy import String, Boolean, Date, ForeignKey
# from app.core.database import Base

# class DinnerGuests(Base):
#     __tablename__ = "dinner_guests"
    
#     id: Mapped[int] = mapped_column(primary_key=True)
    
#     friend_of: Mapped[str] = mapped_column(ForeignKey("tenants.id"))
    
#     name: Mapped[str] = mapped_column(String, default="Guest")
    
#     tenant: Mapped["Tenants"] = relationship()
