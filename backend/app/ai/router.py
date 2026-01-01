from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.ai.schemas import AskRequest, AskResponse
from app.ai.service import ask_ai

# This router provides the /ai/ask endpoint (separate from /ai/generate_design)
router = APIRouter(prefix="/ai", tags=["AI-Ask"])

@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, user=Depends(get_current_user)):
    return ask_ai(
        query=request.query,
        user_id=user.id
    )
