from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
# Import other routers - using direct imports for stability
try:
    from app.api.projects import router as projects_router
except ImportError:
    projects_router = None

try:
    from app.api.ai import router as ai_router
except ImportError:
    ai_router = None

from app.core.database import Base, engine

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Architectural Design Assistant")

# --- CORS CONFIGURATION ---
# Handles both localhost and 127.0.0.1 across common React ports
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

# --- DEBUG LOGGER ---
# This will show the exact URL and Status in your terminal
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG: Incoming {request.method} to {request.url}")
    response = await call_next(request)
    print(f"DEBUG: Response Status: {response.status_code}")
    return response

# --- ROUTER REGISTRATION ---

# 1. Auth: Prefix "/auth" is defined inside app/api/auth.py
app.include_router(auth_router)

# 2. Projects: Prefix "/projects" is defined inside app/api/projects.py
if projects_router:
    app.include_router(projects_router)
else:
    print("WARNING: projects_router could not be loaded")

# 3. AI: Prefix "/ai" is defined inside app/api/ai.py
if ai_router:
    app.include_router(ai_router)
else:
    print("WARNING: ai_router could not be loaded")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend is reachable"}