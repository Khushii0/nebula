@echo off
echo Checking if backend is accessible...
echo.

echo Testing http://localhost:8000/health...
curl http://localhost:8000/health 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Backend is running and accessible!
) else (
    echo.
    echo [ERROR] Backend is not accessible at http://localhost:8000
    echo Make sure the backend is running.
)

echo.
echo Testing http://127.0.0.1:8000/health...
curl http://127.0.0.1:8000/health 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Backend is accessible via 127.0.0.1!
) else (
    echo.
    echo [ERROR] Backend is not accessible via 127.0.0.1:8000
)

pause


