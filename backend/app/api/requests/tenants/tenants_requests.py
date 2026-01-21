from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class CreateTenantRequest(BaseModel):
    # id: int
    email: str
    room_number: str
    name: str
    birthday: date
    active: Optional[bool] = True

class UpdateTenantRequest(BaseModel):
    id: int
    email: Optional[str] = None
    room_number: Optional[str] = None
    name: Optional[str] = None
    birthday: Optional[date] = None

class DeactivateTenantRequest(BaseModel):
    id: int
    room_number: str
    
class UpdateTenantPreferencesRequest(BaseModel):
    tenant_id: int
    available_weekdays: Optional[List[int]] = None 
    available_months: Optional[List[int]] = None 
    unavailable_dates_current_month: Optional[List[int]] = None

class UpdateTenantAllergiesRequest(BaseModel):
    tenant_id: int
    allergies: List[int]
    
    