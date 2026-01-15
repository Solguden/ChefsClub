from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.core.database import Base

class Allergies(Base):
    __tablename__ = "allergies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    