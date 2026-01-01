from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    owner_id: int
    sketch_data: Optional[str] = None
    design_concept_url: Optional[str] = None
    design_narrative: Optional[str] = None
    compliance_notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
