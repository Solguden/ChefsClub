from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class UpdateTenantAllergiesRequest(BaseModel):
    tenant_id: int
    allergies: List[int]