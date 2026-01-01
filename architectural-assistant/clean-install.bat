@echo off
echo Cleaning and reinstalling dependencies...
echo.

cd /d %~dp0

echo Deleting node_modules...
if exist node_modules (
    rmdir /s /q node_modules
    echo node_modules deleted
) else (
    echo node_modules does not exist
)

echo.
echo Deleting package-lock.json...
if exist package-lock.json (
    del package-lock.json
    echo package-lock.json deleted
) else (
    echo package-lock.json does not exist
)

echo.
echo Running npm install...
npm install

echo.
echo Done!
pause


