# Quick Start Guide

## Prerequisites
- Python 3.8+ installed
- Node.js 14+ and npm installed

## Step 1: Start Backend

Open a terminal in the `backend` directory:

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Linux/Mac:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend will start on `http://localhost:8000`
API docs: `http://localhost:8000/docs`

## Step 2: Start Frontend

Open a **new terminal** in the `architectural-assistant` directory:

```bash
cd architectural-assistant
npm install
npm start
```

The frontend will start on `http://localhost:3000`

## Step 3: Use the Application

1. Open `http://localhost:3000` in your browser
2. Register a new account (or login if you have one)
3. Click "+ New Project" to create a project
4. Enter a design brief (e.g., "Modern 3-bedroom house with open kitchen")
5. Optionally draw a sketch
6. Click "Generate Design" to get AI-generated design concepts

## Troubleshooting

### Backend won't start
- Make sure you activated the virtual environment
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)

### Frontend won't start
- Make sure Node.js is installed: `node --version`
- Install dependencies: `npm install`
- Check for port conflicts (3000 should be available)

### CORS errors
- Make sure backend is running on port 8000
- Check that `CORS_ORIGINS` in backend includes `http://localhost:3000`

### Database errors
- The app uses SQLite by default (creates `architect.db` automatically)
- Make sure the backend directory has write permissions

## Default Configuration

The app runs in **mock mode** by default, which means:
- ✅ No API keys required
- ✅ Works offline
- ✅ Returns sample design responses
- ✅ Perfect for testing

To enable real AI features, edit `backend/.env`:
```
LLM_MODE=openai
OPENAI_API_KEY=your-key-here
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API at `http://localhost:8000/docs`
- Check the code structure in `backend/app/` and `architectural-assistant/src/`

