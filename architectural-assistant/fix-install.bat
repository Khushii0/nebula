@echo off
echo ========================================
echo Fixing npm install issues
echo ========================================
echo.

cd /d %~dp0

echo Step 1: Deleting node_modules...
if exist node_modules (
    rmdir /s /q node_modules
    echo   [OK] node_modules deleted
) else (
    echo   [SKIP] node_modules does not exist
)

echo.
echo Step 2: Deleting package-lock.json...
if exist package-lock.json (
    del /q package-lock.json
    echo   [OK] package-lock.json deleted
) else (
    echo   [SKIP] package-lock.json does not exist
)

echo.
echo Step 3: Verifying package.json versions...
findstr /C:"@react-three/drei" package.json | findstr /C:"9.88"
if %ERRORLEVEL% EQU 0 (
    echo   [OK] @react-three/drei version is correct (9.88.13)
) else (
    echo   [ERROR] @react-three/drei version mismatch!
)

findstr /C:"@react-three/fiber" package.json | findstr /C:"8.15"
if %ERRORLEVEL% EQU 0 (
    echo   [OK] @react-three/fiber version is correct (8.15.11)
) else (
    echo   [ERROR] @react-three/fiber version mismatch!
)

findstr /C:"\"react\"" package.json | findstr /C:"17.0"
if %ERRORLEVEL% EQU 0 (
    echo   [OK] React version is correct (17.0.2)
) else (
    echo   [ERROR] React version mismatch!
)

echo.
echo Step 4: Running npm install...
echo   This may take a few minutes...
npm install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo [SUCCESS] Installation completed!
    echo ========================================
    echo.
    echo You can now run: npm start
) else (
    echo.
    echo ========================================
    echo [ERROR] Installation failed!
    echo ========================================
    echo.
    echo Please check the error messages above.
)

pause


