@echo off
echo Starting Architectural Design Assistant Backend...
echo.
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.
echo Starting server on http://localhost:8000
echo API docs available at http://localhost:8000/docs
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

