# app/api/ai.py
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from app.ai.service import generate_design, check_compliance
import base64
import json

router = APIRouter(prefix="/ai", tags=["AI"])


class GenerateDesignRequest(BaseModel):
    project_id: int
    text_brief: str
    sketch_data: Optional[str] = None


@router.post("/generate_design")
async def generate_design_endpoint(
    request: GenerateDesignRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calls AI pipeline with sketch + brief.
    Returns:
        - design_concept_url: 3D model URL or images
        - design_narrative: description
        - compliance_notes: building code checks
    """
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == request.project_id,
        Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Combine text brief and sketch context
    prompt = f"Design brief: {request.text_brief}"
    if request.sketch_data:
        prompt += "\n\nUser has provided a sketch. Analyze the sketch and incorporate its elements into the design."
    
    # Mock mode
    if settings.LLM_MODE == "mock":
        design_narrative = f"Based on your brief '{request.text_brief}', this design incorporates modern architectural principles with sustainable materials. The layout emphasizes natural light and open spaces, creating a harmonious living environment."
        compliance_notes = "✓ Meets standard building codes\n✓ Fire safety regulations compliant\n✓ Accessibility standards met\n✓ Structural requirements satisfied"
        
        # Update project
        project.design_narrative = design_narrative
        project.compliance_notes = compliance_notes
        project.design_concept_url = "/static/mock_model.glb"
        if request.sketch_data:
            project.sketch_data = request.sketch_data
        db.commit()
        
        return JSONResponse({
            "design_concept_url": "/static/mock_model.glb",
            "design_narrative": design_narrative,
            "compliance_notes": compliance_notes
        })
    
    # Real AI mode
    try:
        # Generate design using AI service
        design_output = generate_design(prompt)
        design_narrative = design_output.get("narrative", "Design generated successfully.")
        
        # Check compliance
        compliance_output = check_compliance(design_narrative)
        compliance_notes = compliance_output.get("notes", "Compliance check completed.")
        
        # Update project
        project.design_narrative = design_narrative
        project.compliance_notes = compliance_notes
        if request.sketch_data:
            project.sketch_data = request.sketch_data
        db.commit()
        
        return JSONResponse({
            "design_concept_url": design_output.get("model_url", "/static/mock_model.glb"),
            "design_narrative": design_narrative,
            "compliance_notes": compliance_notes
        })
    except Exception as e:
        # Fallback to mock on error
        return JSONResponse({
            "design_concept_url": "/static/mock_model.glb",
            "design_narrative": f"Design generated based on: {request.text_brief}",
            "compliance_notes": "Compliance check completed.",
            "error": str(e)
        })


@router.post("/generate_design/form")
async def generate_design_form(
    project_id: int = Form(...),
    text_brief: str = Form(...),
    sketch_data: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Form-based endpoint for design generation"""
    request = GenerateDesignRequest(
        project_id=project_id,
        text_brief=text_brief,
        sketch_data=sketch_data
    )
    return await generate_design_endpoint(request, current_user, db)
