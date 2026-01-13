from pydantic import BaseModel
from typing import Optional

class TenantCreate(BaseModel):
    room_number: str
    name: str
    birthday: str
    active: Optional[bool] = True

class TenantUpdate(BaseModel):
    room_number: str
    name: Optional[str] = None
    birthday: Optional[str] = None

class TenantDeactivate(BaseModel):
    room_number: str
    active: bool