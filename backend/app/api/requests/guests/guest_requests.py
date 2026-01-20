from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class CreateGuestRequest(BaseModel):
    tenant_id: int
    name: str
    
class UpdateGuestAllergiesRequest(BaseModel):
    guest_id: int
    allergies: List[int]