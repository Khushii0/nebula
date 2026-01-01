from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password, create_access_token, verify_token, get_current_user
)
from app.models.user import User
from app.core.config import settings
import httpx

router = APIRouter(prefix="/auth", tags=["Auth"])


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str = ""


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # #region agent log
    import json
    log_path = r"d:\codes\nebula\.cursor\debug.log"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"location":"auth.py:register:entry","message":"Register endpoint called","data":{"email":user_data.email,"hasName":bool(user_data.name)},"timestamp":__import__("time").time()*1000,"sessionId":"debug-session","runId":"register-attempt","hypothesisId":"BACKEND"}) + "\n")
    except: pass
    # #endregion
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        # #region agent log
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"location":"auth.py:register:user-exists","message":"User already exists","data":{"email":user_data.email},"timestamp":__import__("time").time()*1000,"sessionId":"debug-session","runId":"register-attempt","hypothesisId":"BACKEND"}) + "\n")
        except: pass
        # #endregion
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_pwd = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        name=user_data.name or user_data.email.split("@")[0],
        provider="local"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create token
    token = create_access_token(data={"sub": user.id})
    # #region agent log
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"location":"auth.py:register:success","message":"User registered successfully","data":{"userId":user.id,"email":user.email},"timestamp":__import__("time").time()*1000,"sessionId":"debug-session","runId":"register-attempt","hypothesisId":"BACKEND"}) + "\n")
    except: pass
    # #endregion
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email
    )


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token = create_access_token(data={"sub": user.id})
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email
    )


@router.post("/login/json", response_model=TokenResponse)
def login_json(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token = create_access_token(data={"sub": user.id})
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email
    )


@router.get("/me")
def get_current_user_info(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "provider": user.provider
    }


# OAuth endpoints (simplified - full implementation would require proper OAuth flow)
@router.get("/oauth/google")
async def oauth_google_redirect():
    """Redirect to Google OAuth"""
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Google OAuth not configured")
    # In production, redirect to Google OAuth URL
    return {"message": "Google OAuth not fully implemented - use local auth"}


@router.get("/oauth/github")
async def oauth_github_redirect():
    """Redirect to GitHub OAuth"""
    if not settings.GITHUB_CLIENT_ID:
        raise HTTPException(status_code=503, detail="GitHub OAuth not configured")
    # In production, redirect to GitHub OAuth URL
    return {"message": "GitHub OAuth not fully implemented - use local auth"}


@router.get("/ping")
def ping():
    return {"ok": True}
