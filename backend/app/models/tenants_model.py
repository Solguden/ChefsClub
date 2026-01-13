from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from app.core.database import Base

class Tenants(Base):
    __tablename__ = "tenants"
    
    room_number: Mapped[str] = mapped_column(String,primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    birthday: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean, unique=False, default=True)
    