from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.ai import router as ai_router
from app.core.database import Base, engine

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Architectural Assistant API")

# 1. FIXED CORS CONFIGURATION
# We list the exact origins your browser is using.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. DEBUG MIDDLEWARE
# This will show you in the terminal EXACTLY what URL the frontend is hitting.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG: Incoming {request.method} request to {request.url}")
    response = await call_next(request)
    print(f"DEBUG: Response Status: {response.status_code}")
    return response

# 3. ROUTER REGISTRATION (NO DOUBLE PREFIXES)
# Since auth.py ALREADY has prefix="/auth", we include it here WITHOUT a prefix.
# This makes the URL: http://localhost:8000/auth/register
app.include_router(auth_router)

# For projects and ai, check if they have prefixes inside their files. 
# If they DON'T, add them here. If they DO, remove the prefix below.
app.include_router(projects_router, prefix="/projects")
app.include_router(ai_router, prefix="/ai")

@app.get("/")
def root():
    return {"status": "online", "message": "Backend is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}