# How to Run the Architectural Design Assistant

## Prerequisites

- **Python 3.8 or higher** installed
- **Node.js 14+ and npm** installed
- **Git** (optional, for cloning)

## Step-by-Step Instructions

### 1. Backend Setup

Open a **terminal/command prompt** and navigate to the backend folder:

```bash
cd backend
```

#### Windows:
```bash
# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

#### Linux/Mac:
```bash
# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

**✅ Backend is running when you see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Backend API will be available at:**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

### 2. Frontend Setup

Open a **NEW terminal/command prompt** (keep backend running) and navigate to the frontend folder:

```bash
cd architectural-assistant
```

```bash
# Install dependencies (first time only)
npm install

# Start the development server
npm start
```

**✅ Frontend is running when you see:**
```
Compiled successfully!
You can now view architectural-assistant in the browser.
  Local:            http://localhost:3000
```

The browser should automatically open to http://localhost:3000

---

### 3. Using the Application

1. **Register/Login**
   - If you're new, click "Register" and create an account
   - If you have an account, click "Login"
   - Enter your email and password

2. **Create a Project**
   - Click the "+ New Project" button
   - Enter a project title (e.g., "Modern House Design")
   - Optionally add a description
   - Click "Create"

3. **Enter Design Brief**
   - In the text area, describe your design requirements
   - Example: "Modern 3-bedroom house with open kitchen, large windows, and sustainable materials"

4. **Draw a Sketch (Optional)**
   - Use the sketch canvas to draw a rough design
   - Click "Save Sketch" when done

5. **Generate Design**
   - Click the "Generate Design" button
   - Wait a few seconds for the AI to process
   - View the results:
     - **Design Narrative**: Detailed description of the design
     - **Compliance Notes**: Building code compliance information
     - **3D Preview**: Visual representation (placeholder)

---

## Quick Start Scripts

### Windows

**Backend:**
```bash
cd backend
start.bat
```

**Frontend:**
```bash
cd architectural-assistant
start.bat
```

### Linux/Mac

**Backend:**
```bash
cd backend
chmod +x start.sh
./start.sh
```

**Frontend:**
```bash
cd architectural-assistant
npm install
npm start
```

---

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError"**
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "Port 8000 already in use"**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
# Then update frontend axios baseURL to http://localhost:8001
```

**Error: "Database locked" (SQLite)**
- Close any other processes using the database
- Delete `architect.db` and restart (will recreate)

### Frontend Issues

**Error: "Cannot find module"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules  # Linux/Mac
# or
rmdir /s node_modules  # Windows

npm install
```

**Error: "Port 3000 already in use"**
```bash
# Use a different port
PORT=3001 npm start  # Linux/Mac
# Windows: set PORT=3001 && npm start
```

**CORS Errors**
- Make sure backend is running on port 8000
- Check browser console for specific error
- Verify `CORS_ORIGINS` in backend includes `http://localhost:3000`

### General Issues

**"Network Error" or "Connection Refused"**
- Verify backend is running (check http://localhost:8000/health)
- Check that frontend axios baseURL is correct (should be `http://localhost:8000`)

**Authentication not working**
- Clear browser localStorage: `localStorage.clear()` in browser console
- Try registering a new account
- Check backend logs for errors

**Design generation returns mock data**
- This is normal! The app runs in "mock" mode by default
- To use real AI, set `OPENAI_API_KEY` in backend/.env and `LLM_MODE=openai`

---

## Configuration

### Backend Environment Variables

Create `backend/.env` file (optional - defaults work):

```env
# Database (SQLite by default)
DATABASE_URL=sqlite:///./architect.db

# Security (change in production!)
SECRET_KEY=your-secret-key-min-32-chars

# AI (optional - for real AI features)
OPENAI_API_KEY=your-key-here
LLM_MODE=mock  # or "openai" for real AI
EMBEDDING_MODE=mock

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend Configuration

The frontend is configured to connect to `http://localhost:8000` by default.

To change the backend URL, edit `architectural-assistant/src/App.tsx`:
```typescript
axios.defaults.baseURL = 'http://localhost:8000';  // Change this
```

---

## Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ is installed: `python --version`
- [ ] Node.js 14+ is installed: `node --version`
- [ ] Backend virtual environment is activated
- [ ] All backend dependencies installed: `pip list` shows fastapi, uvicorn, etc.
- [ ] All frontend dependencies installed: `npm list` shows react, axios, etc.
- [ ] Backend is running: http://localhost:8000/health returns `{"status":"healthy"}`
- [ ] Frontend is running: http://localhost:3000 opens
- [ ] No port conflicts (8000 and 3000 are free)
- [ ] Browser console shows no errors (F12 → Console)

---

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Explore API at http://localhost:8000/docs
- Check code structure in `backend/app/` and `architectural-assistant/src/`

---

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review backend logs in the terminal
3. Check browser console (F12) for frontend errors
4. Verify all prerequisites are installed correctly



