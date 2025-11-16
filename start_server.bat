@echo off
REM Quick Start Script for AI Extraction Testing
REM Run this to start the local testing server

echo.
echo ========================================
echo   AI EXTRACTION TESTING - QUICK START
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo.
    echo Please create a .env file with your Gemini API key:
    echo GEMINI_API_KEY=your_api_key_here
    echo.
    echo Get your API key from: https://aistudio.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking .env file... OK
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [2/3] Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo [2/3] Dependencies already installed... OK
)
echo.

echo [3/3] Starting server...
echo.
echo ========================================
echo   SERVER WILL START IN 2 SECONDS
echo ========================================
echo.
echo  Open your browser and go to:
echo  http://localhost:5000
echo.
echo  Press Ctrl+C to stop the server
echo.
timeout /t 2 /nobreak >nul

python app.py
