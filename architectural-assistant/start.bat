@echo off
echo Starting Architectural Design Assistant Frontend...
echo.
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)
echo.
echo Starting development server on http://localhost:3000
echo.
npm start

