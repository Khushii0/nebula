# 🚀 START HERE - Architectural Design Assistant

## Quick Start (3 Steps)

### Step 1: Start Backend

**Open Terminal 1:**

```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
# OR: source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

✅ Wait for: `Uvicorn running on http://127.0.0.1:8000`

---

### Step 2: Start Frontend

**Open Terminal 2 (NEW terminal):**

```bash
cd architectural-assistant
npm install
npm start
```

✅ Browser opens to http://localhost:3000

---

### Step 3: Use the App

1. **Register** a new account
2. **Create** a new project
3. **Enter** a design brief (e.g., "Modern 3-bedroom house")
4. **Click** "Generate Design"
5. **View** the results!

---

## That's It! 🎉

The app is now running. For detailed instructions, see [RUN.md](RUN.md)

## Troubleshooting

**Backend won't start?**
- Make sure Python 3.8+ is installed
- Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- Install dependencies: `pip install -r requirements.txt`

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Install dependencies: `npm install`

**Can't connect?**
- Make sure backend is running on port 8000
- Check http://localhost:8000/health in browser
- Verify frontend is on port 3000

---

## Need Help?

See [RUN.md](RUN.md) for detailed troubleshooting and configuration.



