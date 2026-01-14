from pydantic import BaseModel
from typing import Optional

class TenantCreate(BaseModel):
    # id: int
    email: str
    room_number: str
    name: str
    birthday: str
    active: Optional[bool] = True

class TenantUpdate(BaseModel):
    id: int
    email: Optional[str] = None
    room_number: Optional[str] = None
    name: Optional[str] = None
    birthday: Optional[str] = None

class TenantDeactivate(BaseModel):
    id: int
    active: bool