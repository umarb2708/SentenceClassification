@echo off
REM Sentence Classification System - Start Script
REM This script activates the virtual environment and starts the Flask application

echo ========================================
echo  Starting Sentence Classification App
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Please create .env file and add your API keys.
    echo You can copy .env.example to .env and edit it.
    echo.
    pause
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Start Flask application
echo [INFO] Starting Flask application...
echo.
echo ========================================
echo  Application is running!
echo ========================================
echo.
echo Open your browser and go to:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python start_app.py

REM Deactivate virtual environment when done
deactivate
