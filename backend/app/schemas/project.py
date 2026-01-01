from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project 

# We set the prefix here to ensure it matches the /projects/ call
router = APIRouter(prefix="/projects", tags=["Projects"])

class ProjectCreate(BaseModel):
    # This alias ensures it works whether frontend sends "name" or "title"
    title: str = Field(..., alias="name", validation_alias="title")
    description: Optional[str] = ""

    class Config:
        populate_by_name = True

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

# Matches: POST http://localhost:8000/projects/
@router.post("/", response_model=ProjectResponse)
def create_project(
    project_in: ProjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        new_project = Project(
            title=project_in.title,
            description=project_in.description,
            owner_id=current_user.id
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Matches: GET http://localhost:8000/projects/
@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Project).filter(Project.owner_id == current_user.id).all()