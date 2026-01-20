from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class AddDinnerParticipantRequest(BaseModel):
    date: date
    tenant_id: int
    
class AddDinnerGuestRequest(BaseModel):
    date: date
    tenant_id: int
    guest_id: int