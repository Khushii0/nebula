from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, projects, ai
from app.core.database import Base, engine
from app.core.config import settings
import json
import time

# Import all models to ensure they're registered with SQLAlchemy
from app.models import user, project, version

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Architectural Design Assistant",
    description="AI-powered architectural design tool",
    version="1.0.0"
)

# CORS middleware
cors_origins = settings.get_cors_origins()
# #region agent log
log_path = r"d:\codes\nebula\.cursor\debug.log"
try:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"location":"main.py:startup","message":"CORS configuration","data":{"origins":cors_origins},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"startup","hypothesisId":"CORS"}) + "\n")
except: pass
# #endregion
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # #region agent log
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"location":"main.py:middleware:request","message":"Incoming request","data":{"method":request.method,"url":str(request.url),"origin":request.headers.get("origin"),"referer":request.headers.get("referer")},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"request","hypothesisId":"NETWORK"}) + "\n")
    except: pass
    # #endregion
    response = await call_next(request)
    # #region agent log
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"location":"main.py:middleware:response","message":"Outgoing response","data":{"status":response.status_code,"headers":dict(response.headers)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"request","hypothesisId":"NETWORK"}) + "\n")
    except: pass
    # #endregion
    return response

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(ai.router)  # This provides /ai/generate_design

# Include additional AI router for /ai/ask endpoint
try:
    from app.ai.router import router as ai_ask_router
    app.include_router(ai_ask_router)  # This provides /ai/ask
except ImportError:
    pass

@app.get("/")
def root():
    return {"message": "Architectural Design Assistant API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
