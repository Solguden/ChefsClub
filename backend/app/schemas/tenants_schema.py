from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class TenantCreate(BaseModel):
    # id: int
    email: str
    room_number: str
    name: str
    birthday: date
    active: Optional[bool] = True

class TenantUpdate(BaseModel):
    id: int
    email: Optional[str] = None
    room_number: Optional[str] = None
    name: Optional[str] = None
    birthday: Optional[date] = None

class TenantDeactivate(BaseModel):
    id: int
    active: bool
    
class TenantPreferences(BaseModel):
    id: int
    available_weekdays: Optional[List[int]] = None 
    available_months: Optional[List[int]] = None 