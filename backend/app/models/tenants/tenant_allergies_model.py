from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.core.database import Base

class TenantAllergies(Base):
    __tablename__ = "tenant_allergies"
    tenant_id : Mapped[int] = mapped_column(ForeignKey("tenants.id"),primary_key=True)
    allergy_id : Mapped[int] = mapped_column(ForeignKey("allergies.id"),primary_key=True)