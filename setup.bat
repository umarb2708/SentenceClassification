@echo off
REM Sentence Classification System - Setup Script
REM This script sets up the virtual environment and installs all dependencies

echo ========================================
echo  Sentence Classification System Setup
echo ========================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

python --version
echo [SUCCESS] Python is installed!
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python version: %PYTHON_VERSION%
echo.

REM Check if virtual environment already exists
if exist "venv\" (
    echo [WARNING] Virtual environment already exists!
    echo Do you want to recreate it? This will delete the existing environment.
    set /p RECREATE="Type 'yes' to recreate or press Enter to keep existing: "
    if /i "%RECREATE%"=="yes" (
        echo [2/5] Removing existing virtual environment...
        rmdir /s /q venv
        echo [SUCCESS] Removed existing virtual environment.
        echo.
    ) else (
        echo [INFO] Keeping existing virtual environment.
        echo.
        goto :activate_venv
    )
)

REM Create virtual environment
echo [2/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to create virtual environment!
    echo Please make sure Python venv module is installed.
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created!
echo.

:activate_venv
REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated!
echo.

REM Upgrade pip
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [SUCCESS] Pip upgraded!
echo.

REM Install dependencies
echo [5/5] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo Please check requirements.txt and your internet connection.
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] All dependencies installed!
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ========================================
    echo  Environment Configuration Required
    echo ========================================
    echo.
    echo [WARNING] .env file not found!
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo.
    echo [IMPORTANT] Please edit the .env file and add your API keys:
    echo   1. Open .env file in a text editor
    echo   2. Get your Gemini API key from: https://makersuite.google.com/app/apikey
    echo   3. Replace 'your_gemini_api_key_here' with your actual API key
    echo   4. Save the file
    echo.
) else (
    echo [INFO] .env file already exists.
    echo.
)

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Make sure to configure your API key in .env file
echo   2. Run 'start_app.bat' to start the application
echo   3. Open your browser to http://localhost:5000
echo.
echo If you need to activate the virtual environment manually:
echo   venv\Scripts\activate
echo.
pause
